# 本机测试版：3.7.1-local-test1

已编译并覆盖安装，游戏功能尚待用户测试。

- DLL SHA-256：`A631652B6BFCF4EC4230E27EF26D8DEC7401FE5E9D70EEFA142B6BDE842BB044`
- 原版备份目录：`E:\SteamLibrary\steamapps\common\Palworld\Mods\Backups\ziyuan-20261031-154730`
- 运行目录：`Mods/NativeMods/UE4SS/Mods/ziyuan`。
- 当前仍使用 `ziyuan : 1` 加载，不需要另开一个模组。
- 旧 Lua 同步逻辑已停用；Scripts/main.lua 仅输出启动提示。
- 安装清单已记录新 DLL、配置和许可证，原清单保存在备份的 Managed 子目录。

## 测试

1. 完全重启游戏并进入单人存档，等待约 10 秒。
2. 多个据点分别放入木材、石头、矿石等不同物品，玩家背包清空相应材料；在其他据点检查建造与制作的材料数量。
3. 实际建造/制作一次，回来源箱子确认扣除数量正确；材料不足时应正常拒绝。
4. 再测试第三个据点、不同种类储物箱、远处未访问据点，以及新增/拆除箱子和重新进档。

若失败，保留此次 `Mods/NativeMods/UE4SS/UE4SS.log`；需要区分“数量不显示”“显示但不能建造”“能建造但扣错/不扣”和“启动或进档崩溃”。不要用加载成功代替功能验收。

日志应包含四个原生钩子的 `hooked=true`、`3.7.1-local-test1 native hooks installed` 和 `SRV discover`。若包含 `incomplete native resolution`、`installation rolled back` 或 `missing reflected server model map`，该版本未能完成适配，需要继续修正。

## 回退

退出游戏，将运行目录的 `dlls/main.dll` 改名为 `main.dll.disabled`；从备份的 `ziyuan/Scripts/main.lua` 恢复原脚本，从 `Managed/InstallManifest.json` 恢复原安装清单。其余配置和许可证不会自行执行。回退不改动存档。

原始源码另保存在 Git 标签 `resource-share-baseline-v2.3`。
