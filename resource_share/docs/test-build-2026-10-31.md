# 本机测试版：3.7.1-local-test2

已编译并覆盖安装；用户已确认最小跨据点建造及扣料场景成功，其余功能待测。

- DLL SHA-256：`6AC0165C153F32493FD5C9483BC02693F9BD834EBE65CB99B111B7F65398AD56`
- 原版备份目录：`E:\SteamLibrary\steamapps\common\Palworld\Mods\Backups\ziyuan-20261031-154730`
- 运行目录：`Mods/NativeMods/UE4SS/Mods/ziyuan`。
- 当前仍使用 `ziyuan : 1` 加载，不需要另开一个模组。
- 旧 Lua 同步逻辑已停用；Scripts/main.lua 仅输出启动提示。
- 安装清单已记录新 DLL、配置和许可证，原清单保存在备份的 Managed 子目录。

## test1 失败与 test2 修正

用户复现：A 箱子 31 石头，B 没有箱子、没有石头，B 建造不能使用 A 的材料。

本机日志摘录（2026-10-31）：`15:49:22.735 [ISGATE] ERROR: incomplete native resolution; no hooks installed`。因此 test1 的共享原生钩子没有启用，不能据此判断空据点扫描是否有效。

已确认 `FindObject(ClassName, ObjectShortName)` 只比较对象短名称，test1 却给第二个参数传了完整路径。test2 改为在 `OnReadyModuleItemStackInfo` 所属类上调用 `GetFunctionByNameInChain("GetItemStackCount64")`，并输出四个定位 RVA。

只读离线扫描本机游戏 PE，按上游调用关系规则得到：containers `0x2d7e7c0`、camp `0x3009890`、consume `0x2d997a0`、stack `0x3296320`。这些是检查结果，不是写死的补丁地址。反射查找、钩子安装和游戏行为仍需实际启动验证。

编译成功，导出入口存在，56 个 UE4SS 导入全部匹配已安装 DLL，覆盖后 SHA-256 与构建输出一致。上一版备份：`E:\SteamLibrary\steamapps\common\Palworld\Mods\Backups\ziyuan-20261031-155902-test1`。原始 Lua 备份仍保留在上面的原版备份目录。

## 测试

1. 完全重启游戏并进入单人存档，等待约 10 秒。
2. 首先保持用户的复现场景：A 箱子 31 石头、B 无箱子、背包无石头，在 B 检查材料计数并建造，再回 A 确认真实扣料。随后多个据点分别放入木材、石头、矿石等不同物品，玩家背包清空相应材料；在其他据点检查建造与制作的材料数量。
3. 实际建造/制作一次，回来源箱子确认扣除数量正确；材料不足时应正常拒绝。
4. 再测试第三个据点、不同种类储物箱、远处未访问据点，以及新增/拆除箱子和重新进档。

若失败，保留此次 `Mods/NativeMods/UE4SS/UE4SS.log`；需要区分“数量不显示”“显示但不能建造”“能建造但扣错/不扣”和“启动或进档崩溃”。不要用加载成功代替功能验收。

日志应包含四个原生钩子的 `hooked=true`、`3.7.1-local-test2 native hooks installed` 和 `SRV discover`。若包含 `incomplete native resolution`、`installation rolled back` 或 `missing reflected server model map`，该版本未能完成适配，需要继续修正。

## 回退

退出游戏，将运行目录的 `dlls/main.dll` 改名为 `main.dll.disabled`；从备份的 `ziyuan/Scripts/main.lua` 恢复原脚本，从 `Managed/InstallManifest.json` 恢复原安装清单。其余配置和许可证不会自行执行。回退不改动存档。

原始源码另保存在 Git 标签 `resource-share-baseline-v2.3`。

## 用户验收结果（2026-10-31）

**通过：**A 箱子放置 31 个石头；玩家背包无石头；B 没有箱子和石头。用户在 B 查看材料并成功建造，回 A 确认石头按实际成本减少。

同次本机日志确认：四个原生入口全部 `hooked=true`，RVA 与离线检查一致；`ROLE server=1 dedicated=0 -> HOST/SP (server)`；扫描 `chests=2 camps=2 guilds=1 inst=2`。仅记录这段相关摘要，不发布完整运行日志。

未验收：其他材料/箱子类型、三个以上据点、远处未访问据点、制作/生产、材料不足、新增/拆除箱子、重新进档、快速堆叠、物品检索及不同公会隔离。不能把上述一项通过扩展为全部功能通过。多人和专用服务器不在已验证范围。

本次发行沿用同一个 DLL（SHA-256 不变），版本 `3.7.1-local-test2`，标记为 GitHub prerelease；官方 Uploader 包结构已检查，但未执行其安装/上传验收。
