# ziyuan（资源互通）排查记录

日期：2026-10-31（Asia/Shanghai）  
用户提供的游戏版本：Palworld v1.0.5.102999  
游戏模式：本机单人存档（用户确认）

## 结论与证据强度

已确认 mod 加载、事件钩子注册和初始对象扫描均执行过。最可能的主因是旧版 IntegratedStorage v2.3 Lua 实现缺少 Palworld 1.0.5 的跨基地材料查询、扣料及配方数量适配。当前安装的脚本只做箱子交叉注册；上游 1.0.5 修复源码明确处理了交叉注册后仍被游戏按基地归属过滤的问题。

这是本机日志、脚本审查和上游修复记录共同支持的高可信诊断，尚未通过本机运行时跟踪直接验证过滤分支，也没有完成修复后的游戏验收。本次排查未启动游戏、未修改运行中的库存或存档、未替换 mod。

## 本机已确认事实

- `Mods/ManagedMods/ziyuan/Info.json` 是安装元数据：名称“资源互通”，包名 `ziyuan`，包版本 `1.0.0`，作者“梅川库梓”，最低 Revision `82182`，Lua 安装规则。最低版本声明不能证明它兼容之后的所有版本。
- 实际执行文件 `Mods/NativeMods/UE4SS/Mods/ziyuan/Scripts/main.lua` 第 1 行标识为 **IntegratedStorage v2.3**，原作者 Sarfflow。包版本与脚本版本是两套编号。
- `Mods/NativeMods/UE4SS/Mods/mods.txt` 第 29 行为 `ziyuan : 1`。即使 `mods.json` 没有列出它，本次日志已直接证明它成功加载。
- UE4SS 为 `v3.0.1 Beta #0`，Git SHA `2281fa31`。
- 排查时未检测到 Palworld 游戏进程。

日志文件：`Mods/NativeMods/UE4SS/UE4SS.log`。

| 日志行 | 时间 | 证据 |
| --- | --- | --- |
| 1284 | 14:38:49 | `[IntegratedStorage] v2.3 loaded (event-driven, host-side)` |
| 1382 | 14:38:59 | `OnAvailableConcreteModel_ServerInternal` 钩子注册成功 |
| 1383 | 14:38:59 | `OnNotAvailableConcreteModel_ServerInternal` 钩子注册成功 |
| 1415 | 14:39:43 | BaseRadiusImproved 报告本机 `role: authority`，与用户确认的单人模式一致 |
| 1431 | 14:40:09 | `bootstrap complete: 2 storage module(s), 2 chest(s) pooled` |

## 失效机制

脚本第 148 行对各基地库存模块调用 `OnAvailableConcreteModel_ServerInternal(m)`，将同公会箱子交叉注册。它没有处理材料查询或实际扣料时的基地归属过滤，也没有补足配方列表读取的跨基地物品数量。

[上游 PR #5：1.0.5 compatibility update](https://github.com/Sarfflow/palworld-integrated-storage/pull/5) 说明：交叉注册的箱子仍会因其实际所属基地不同而被过滤，导致菜单和实际建造仍只能使用本基地库存。

已核对该 PR 的 [固定提交源码](https://github.com/IanMoroney/palworld-integrated-storage/blob/6a3de750da7d416a2b02d1852c3dac27d21a6b8b/src/dllmain.cpp)：

- 第 713–772 行：在容器查询和实际扣料的限定调用范围内，为同公会箱子处理基地归属过滤。
- 第 734–758 行：处理 `GetItemStackCount64` 的跨基地数量，以修正配方图标的材料判定。
- 该实现使用 C++ 原生函数 detour。仅改 JSON、提高扫描频率或再加一次现有 Lua 注册调用，并未覆盖这些适配点。

排查时 PR 仍为 open、尚未合并；提交者在[评论](https://github.com/Sarfflow/palworld-integrated-storage/pull/5#issuecomment-5847734802)中报告测试成功。这不能替代对本机精确版本及现有其他 mod 的兼容性验证。

另有[社区修复版页面](https://www.nexusmods.com/palworld/mods/5262?tab=description)说明了 1.0.4 后跨基地材料不计入的问题，但其页面标注的验证版本为 1.0.4，不能据此保证其二进制适用于本机 1.0.5.102999。

## 脚本中的诊断盲点

第 148 行使用 `pcall` 调用注册函数，却忽略成功标志与错误信息，而且无论调用是否成功都执行 `regs = regs + 1`。第 208 行的完成日志只输出扫描得到的基地和箱子数量，没有检查最终可用材料或实际扣料结果。因此，“2 个基地、2 个箱子 pooled”证明对象被识别，不能证明跨基地建造可用。

另外，脚本在最多 3 次有效扫描后结束初始化，之后约 10 分钟才做一次全量补扫。较晚加载的基地是否及时加入取决于事件钩子。这是覆盖率方面的次要疑点，现有日志不足以证明它是本次主因。

日志中另有 PalSchema 的签名查找错误，但没有证据将其归为 ziyuan 失效的直接原因。

## 修复与验收方向

修复应基于 1.0.5 对应接口，同时覆盖同公会跨基地容器查询、真实扣料和配方数量显示。可参考上述 PR 的原生适配实现；不能把当前 v2.3 Lua 文件的加载成功当作兼容性验证。

准备替换实现时保留原脚本与配置备份，并让同一时间只有一套跨基地库存实现运行。验收至少包括：

1. A 基地箱子放入 10 个石头；玩家背包、B 基地及其他共享容器不放石头。
2. 在 B 基地检查建造菜单计数，执行一次需要石头且总成本不超过 10 的建造；确认 A 的石头按配方真实减少。
3. 检查工作台/生产配方显示及扣料，以及材料不足时的正常拒绝行为。
4. 检查新增/拆除箱子、传送、返回标题后重进存档，以及快速堆叠和物品检索功能。

## 原文件校验

`main.lua` SHA-256：

```text
0B5645E5752F9AB817D0D774A90C50C96C880DCFBC9D784F7D50DF38B4525F1A
```

## MCP 查询记录

本次使用 GitHub MCP 读取公开源码与 PR，没有调用 Mathematica/Wolfram，因而没有 Wolfram 命令。关键查询如下：

```javascript
tools.mcp__codex_apps__github_fetch({
  url: "https://github.com/Sarfflow/palworld-integrated-storage/blob/main/src/dllmain.cpp"
});
tools.mcp__codex_apps__github_fetch({
  url: "https://github.com/Sarfflow/palworld-integrated-storage/pull/5"
});
tools.mcp__codex_apps__github_fetch({
  url: "https://github.com/IanMoroney/palworld-integrated-storage/blob/6a3de750da7d416a2b02d1852c3dac27d21a6b8b/src/dllmain.cpp"
});
tools.mcp__codex_apps__github_fetch({
  url: "https://github.com/Sarfflow/palworld-integrated-storage/issues/5"
});
tools.mcp__codex_apps__github_fetch_issue_comments({
  repo_full_name: "Sarfflow/palworld-integrated-storage",
  issue_number: 5
});
```
