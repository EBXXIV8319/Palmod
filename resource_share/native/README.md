# Native compatibility candidate: 3.7.1-local-test1

Compiled and deployed on 2026-10-31 for Palworld 1.0.5.102999 / UE4SS 2281fa31, local single-player. Gameplay validation is pending the user. This is a test candidate, not a verified release.

## Changes

- Adapted PR #5 (6a3de750da7d416a2b02d1852c3dac27d21a6b8b); unchanged reference and MIT license are in reference/.
- Native container query, camp ownership filter, consume and recipe count hooks.
- Same-guild grouping, no item-ID whitelist or fixed camp count.
- Discovery runs on the game thread every two seconds; clears state before map changes; unregisters lifecycle callbacks on unload.
- Reflected map, guild, module, container and slot properties replace hard-coded offsets in the authority scan. StaticId inside ItemId is also located by reflection.
- Avoids dereferencing cached camp pointers for recipe guild comparisons.
- Incomplete address resolution leaves hooks uninstalled; partial detour installation is rolled back.
- Uses MinHook (license in MINHOOK-LICENSE.txt). Remote-client display detours and RPC registration are disabled in this local test build.
- Old Lua registration is replaced by a launcher message to avoid two simultaneous implementations.

## Build

Run `python resource_share/native/build.py` from the repository. Build dependencies are local and ignored; no private SDK code is published here. build.py uses the existing Visual Studio compiler, portable Windows SDK, matching UE4SS headers, and an import library generated from the installed UE4SS.dll.

The portable SDK is under build/winsdk; dependency versions are recorded in dependencies.json. Initial dependency access requires Epic/GitHub authorization. The build cache also contains the reference upstream UE4SS source and xwin download cache.

## Validation performed

- MSVC x64 Shipping/MD build succeeded.
- start_mod and uninstall_mod exports checked.
- All 58 UE4SS import symbols matched installed UE4SS.dll exports.
- Deployed DLL SHA-256 verified against build output.
- Original main.lua backup hash matched the original baseline.

## Pending / limitations

The native resolver uses upstream reflected-function/call-frequency heuristics; its matches have not yet been validated in the running game. All four hook messages must report hooked=true. This version does not claim remote-client support. Coverage of all storage variants and never-visited distant camps remains to be tested. Recipe snapshot counts may take up to two seconds to refresh; native consumption uses actual containers. Source comments in the upstream-derived file retain some description of dormant client functionality.

This prototype must not be hot-reloaded. Restart the game for each deployment.
