-- IntegratedStorage v2.3 - Palworld 1.0 (UE4SS/Lua)
-- Author: Sarfflow
-- Shares every base camp of a guild into one pool, so building/crafting at any camp can
-- use materials stored in any of that guild's chests. Event-driven, host/server-side.

local CHEST_CLASS     = "PalMapObjectItemChestModel"
local TICK_MS         = 10000  -- driver cadence (10s): bootstrap retry interval AND the insurance clock
local INIT_STABLE     = 2      -- populated world: latch once counts are unchanged this many scans
local INIT_MAX        = 3      -- HARD CAP: at most this many bootstrap scans ever (then latch no matter what)
local INSURANCE_TICKS = 60     -- fallback full-scan resync cadence in ticks (60 x 10s = ~10 min)
local STATUS_EVERY    = 6       -- VERBOSE status-log cadence in ticks (~1 min)
local VERBOSE         = false    -- dev logging; the release build flips this to false

-- guilds[gkey] = { storages = { [fullname]=obj }, models = { [fullname]=chest } }
local guilds    = {}
local injecting = false      -- re-entrancy guard: our own re-registration calls re-fire the hooks
local initDone  = false
local bootScans = 0          -- bootstrap scans run so far (reset on level load); backs INIT_MAX
local stableStreak, lastSig, steadyTick = 0, -1, 0   -- bootstrap settle + steady-tick counters (reset on level load)
local stats     = { events = 0, removed = 0, reconciles = 0, lastMs = 0, lastFindMs = 0 }

local function log(fmt, ...) print("[IntegratedStorage] " .. string.format(fmt, ...)) end

-- guild id: FGuid returned by-value from the getter comes back as a safe Lua table {A,B,C,D}
local function guildKey(camp)
    if not camp or not camp:IsValid() then return nil end
    local ok, g = pcall(function() return camp:GetGroupIdBelongTo() end)
    if not ok or type(g) ~= "table" then return nil end
    return string.format("%s_%s_%s_%s", tostring(g.A), tostring(g.B), tostring(g.C), tostring(g.D))
end

local function fullName(o) local ok, n = pcall(function() return o:GetFullName() end); return ok and n or nil end

-- native hook params may arrive as the UObject or wrapped in a RemoteUnrealParam
local function unwrap(p)
    if p == nil or type(p) ~= "userdata" then return p end
    if pcall(function() return p:IsValid() end) then return p end
    local ok, inner = pcall(function() return p:get() end); return ok and inner or p
end

-- chest class or any subclass (matches FindAllOf; excludes non-chest container models)
local function isChest(model)
    local ok, cls = pcall(function() return model:GetClass() end)
    if not ok or not cls then return false end
    while cls and cls:IsValid() do
        if cls:GetFName():ToString() == CHEST_CLASS then return true end
        local sok, sup = pcall(function() return cls:GetSuperStruct() end)
        if not sok then break end
        cls = sup
    end
    return false
end

local function guildOf(k)
    local g = guilds[k]; if not g then g = { storages = {}, models = {} }; guilds[k] = g end; return g
end

-- a chest came online (built at runtime): cross-register it into the other camps of its guild
local function onAvailable(self, model)
    if injecting then return end
    self, model = unwrap(self), unwrap(model)
    if not self or not model or not isChest(model) then return end
    local ok, camp = pcall(function() return self:GetOuter() end); if not ok then return end
    local gk = guildKey(camp); if not gk then return end
    local sk, mk = fullName(self), fullName(model); if not sk or not mk then return end
    local g = guildOf(gk)
    local newStorage = (g.storages[sk] == nil)
    local newModel   = (g.models[mk] == nil)    -- log only the first time we see a chest, mirroring onNotAvailable
    g.storages[sk] = self; g.models[mk] = model
    injecting = true
    local reg = 0
    for k, s in pairs(g.storages) do
        if k ~= sk then
            if s:IsValid() then pcall(function() s:OnAvailableConcreteModel_ServerInternal(model) end); reg = reg + 1 else g.storages[k] = nil end
        end
    end
    if newStorage then                          -- backfill a newly-seen camp with the guild's known chests
        for k, m in pairs(g.models) do
            if k ~= mk then
                if m:IsValid() then pcall(function() self:OnAvailableConcreteModel_ServerInternal(m) end) else g.models[k] = nil end
            end
        end
    end
    injecting = false
    stats.events = stats.events + 1
    if VERBOSE and newModel then log("tracked chest %s -> registered into %d other camp(s)", mk:match("[^%.]+$") or "?", reg) end
end

-- a chest went away: cross-unregister it. The game fires this several times per destroy
-- (the chest is registered in several camps), so act once, only on a chest we track.
local function onNotAvailable(self, model)
    if injecting then return end
    self, model = unwrap(self), unwrap(model)
    if not self or not model or not isChest(model) then return end
    local ok, camp = pcall(function() return self:GetOuter() end); if not ok then return end
    local gk = guildKey(camp); if not gk then return end
    local g = guilds[gk]; if not g then return end
    local sk, mk = fullName(self), fullName(model)
    if not mk or g.models[mk] == nil then return end
    g.models[mk] = nil
    injecting = true
    local unreg = 0
    for k, s in pairs(g.storages) do
        if k ~= sk then
            if s:IsValid() then pcall(function() s:OnNotAvailableConcreteModel_ServerInternal(model) end); unreg = unreg + 1 else g.storages[k] = nil end
        end
    end
    injecting = false
    stats.events = stats.events + 1
    stats.removed = stats.removed + 1
    if VERBOSE then log("untracked chest %s -> unregistered from %d other camp(s)", mk:match("[^%.]+$") or "?", unreg) end
end

-- full scan of the world; cross-registers every guild's chests into every same-guild camp.
-- Returns storageCount, chestCount so the driver can tell when the world has finished loading.
-- Host/server only. Called only by the (bounded, <=INIT_MAX) bootstrap and the ~10-min insurance.
local function reconcile(reason)
    if not FindFirstOf("PalItemContainerManager") then return nil end
    local t0 = os.clock()
    local chests   = FindAllOf(CHEST_CLASS)
    local storages = FindAllOf("PalBaseCampModuleItemStorage")
    local tFind = os.clock()
    if not chests or not storages then return nil end
    local fresh = {}
    local function gf(k) local g = fresh[k]; if not g then g = { storages = {}, models = {} }; fresh[k] = g end; return g end
    local chestCount, storageCount = 0, 0
    for _, ch in pairs(chests) do
        if ch:IsValid() then
            local ok, camp = pcall(function() return ch:GetBaseCampModelBelongTo() end)
            if ok and camp and camp:IsValid() then
                local k = guildKey(camp); if k then local mk = fullName(ch); if mk then gf(k).models[mk] = ch; chestCount = chestCount + 1 end end
            end
        end
    end
    for _, s in pairs(storages) do
        if s:IsValid() then
            local ok, camp = pcall(function() return s:GetOuter() end)
            local k = ok and guildKey(camp)
            if k then local sk = fullName(s); if sk then gf(k).storages[sk] = s; storageCount = storageCount + 1 end end
        end
    end
    injecting = true
    local regs = 0
    for _, g in pairs(fresh) do
        for _, s in pairs(g.storages) do
            if s:IsValid() then
                for _, m in pairs(g.models) do
                    if m:IsValid() then pcall(function() s:OnAvailableConcreteModel_ServerInternal(m) end); regs = regs + 1 end
                end
            end
        end
    end
    injecting = false
    guilds = fresh
    stats.reconciles = stats.reconciles + 1
    stats.lastMs = (os.clock() - t0) * 1000
    stats.lastFindMs = (tFind - t0) * 1000
    if VERBOSE then
        local gc = 0; for _ in pairs(fresh) do gc = gc + 1 end
        log("scan(%s): %.1fms (find %.1fms) guilds=%d storages=%d chests=%d regs=%d",
            reason, stats.lastMs, stats.lastFindMs, gc, storageCount, chestCount, regs)
    end
    return storageCount, chestCount
end

-- level transition frees the whole world; drop stale handles and re-run the bootstrap
local function resetState(reason)
    guilds = {}; injecting = false; initDone = false; bootScans = 0
    stableStreak = 0; lastSig = -1; steadyTick = 0
    if VERBOSE then log("state reset (%s) -> re-running bootstrap on the new world", reason) end
end

local hooked = false
local function ensureHooks()
    if hooked then return true end
    if not StaticFindObject("/Script/Pal.PalBaseCampModuleItemStorage:OnAvailableConcreteModel_ServerInternal") then return false end
    -- the chest build events are the whole maintenance path: they fire when a chest is built (Available)
    -- or removed (NotAvailable) at runtime, so the pool stays correct without any polling or rescans.
    local a = pcall(function() RegisterHook("/Script/Pal.PalBaseCampModuleItemStorage:OnAvailableConcreteModel_ServerInternal", function() end, function(s, m) onAvailable(s, m) end) end)
    local b = pcall(function() RegisterHook("/Script/Pal.PalBaseCampModuleItemStorage:OnNotAvailableConcreteModel_ServerInternal", function() end, function(s, m) onNotAvailable(s, m) end) end)
    hooked = a and b
    if VERBOSE then log("hooks: available=%s notAvailable=%s", tostring(a), tostring(b)) end
    return hooked
end

-- reset before the new world's objects construct (fires the instant a map starts loading)
local okReset = pcall(function() RegisterLoadMapPreHook(function() resetState("LoadMap") end) end)
if VERBOSE and not okReset then log("WARNING: RegisterLoadMapPreHook unavailable") end

-- driver: a tiny bounded bootstrap (<=INIT_MAX scans, one per 10s) to capture chests already present
-- at load, then it latches and never scans again except the ~10-min insurance. Runtime changes ride
-- the build-event hooks above. No per-second work; no client-position-driven rescans.
LoopAsync(TICK_MS, function()
    ExecuteInGameThread(function()
        if not ensureHooks() then return end
        if not initDone then
            local sc, cc = reconcile("bootstrap")
            if not sc then return end           -- container manager not up yet; retry next tick
            bootScans = bootScans + 1
            local sig = sc * 100000 + cc
            stableStreak = (sig == lastSig) and (stableStreak + 1) or 0
            lastSig = sig
            -- latch when a populated world's counts have settled, or at the hard cap no matter what.
            if (sc > 0 and stableStreak >= INIT_STABLE) or (bootScans >= INIT_MAX) then
                initDone = true
                -- one unconditional confirmation (survives the release build) so admins can see the
                -- pool actually captured their camps - "0 storages" here == something wrong
                log("bootstrap complete: %d storage module(s), %d chest(s) pooled; event-driven from here.", sc, cc)
                if VERBOSE then log("authority probe: PalGameMode=%s PalItemContainerManager=%s (a game CLIENT shows GameMode=false)", tostring(FindFirstOf("PalGameMode") ~= nil), tostring(FindFirstOf("PalItemContainerManager") ~= nil)) end
            end
            return
        end
        -- steady state: pure event-driven, plus a ~10-min full-scan insurance resync (the only scan
        -- that runs after latch). Corrects any drift the event path might ever miss.
        steadyTick = steadyTick + 1
        if steadyTick % INSURANCE_TICKS == 0 then
            local sc, cc = reconcile("insurance")
            if VERBOSE and sc then log("insurance resync: %d storages, %d chests", sc, cc) end
        end
        if VERBOSE and steadyTick % STATUS_EVERY == 0 then log("status: events=%d (removed=%d)", stats.events, stats.removed) end
    end)
    return false
end)

print("[IntegratedStorage] v2.3 loaded (event-driven, host-side) - by Sarfflow")
