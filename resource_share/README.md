# resource_share：资源互通

目标：**同一公会的所有据点，都可以使用所有据点储物箱中的全部物品**，用于建造、制作等原生支持的物品消耗，并从实际来源箱子正确扣除。

共享范围不限定物品种类、数量或据点数，不使用石头等固定物品白名单。A 基地有 10 个石头、B 基地可以使用它们，只是便于复现的最小示例。应覆盖多据点、多种储物箱，以及物品在多个箱子中的合计；远处或本次进档后尚未访问的据点也属于目标范围，需要单独验证加载条件与实现限制。

**3.7.1-local-test2 已通过本机单人跨据点建造最小验收：A 有 31 石头、B 无箱子、背包无石头，B 建造成功且 A 按成本扣料。其余场景待测，按预发布版发行。原始 Lua 保存在 resource-share-baseline-v2.3 标签。**

下载 [GitHub Release](https://github.com/EBXXIV8319/Palmod/releases/tag/resource-share-v3.7.1-local-test2)，普通玩家选择 Win64.zip。安装、依赖、升级和卸载见 [发布安装说明](release/README.zh-CN.md)；发布元数据使用 `release/Info.json`，历史 `Info.json` 保持原包快照。

## 原始版本

- 本地安装包：`ziyuan`，显示名称“资源互通”，包版本 `1.0.0`。
- 安装包作者字段：梅川库梓；Workshop ID：`3763145359`。
- 实际 Lua 脚本：IntegratedStorage v2.3，作者 Sarfflow。
- 排查环境：Palworld v1.0.5.102999；UE4SS v3.0.1 Beta #0，Git SHA `2281fa31`。
- 已知现象：模组加载成功且能扫描基地/箱子，但跨基地材料不能用于建造。

## 文件与原始位置

以下路径均相对 Palworld 游戏根目录。

| 本仓库文件 | 原始文件 |
| --- | --- |
| `Scripts/main.lua` | `Mods/NativeMods/UE4SS/Mods/ziyuan/Scripts/main.lua` |
| `Info.json` | `Mods/ManagedMods/ziyuan/Info.json` |
| `InstallManifest.json` | `Mods/ManagedMods/ziyuan/InstallManifest.json` |
| `docs/diagnosis-2026-10-31.md` | `diagnostics/ziyuan-2026-10-31.md` |

初始提交中的前三个文件校验值见 [baseline.sha256](baseline.sha256)。`InstallManifest.json` 是安装来源记录，包含本机安装时间，不应作为运行时配置修改或覆盖回游戏。

原包 `Info.json` 引用了 `thumbnail.png`，但被检查的安装目录中没有此文件。本快照不补造缩略图，也不宣称已是完整可发布安装包。

## 修复入口

- [排查报告](docs/diagnosis-2026-10-31.md)：本地日志证据、上游适配线索和证据边界。
- [日志摘录](docs/ue4ss-evidence.txt)：仅保留与本次加载相关的条目。
- [修复计划与验收](docs/repair-plan.md)：实施前需要确认的接口及功能检查。
- [署名与来源](NOTICE.md)：原作者、分发包和参考实现的区别。

修复已覆盖原生材料查询、实际扣料和配方计数；原始 v2.3 Lua 只交叉注册箱子，且忽略部分 `pcall` 失败结果。当前 Scripts/main.lua 仅为启动提示。

修复与首个预发布版位于 `fix/resource-share-1.0.5` 分支。仓库目前没有接入游戏运行时的自动化测试，语法检查或模拟测试不能替代游戏内验收。
