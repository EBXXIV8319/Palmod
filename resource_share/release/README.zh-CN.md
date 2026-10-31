# 资源互通 / Resource Share — 3.7.1-local-test2

适用于 Palworld **1.0.5.102999 / Windows x64 / 本机单人存档**的预发布版。
目标是在同一公会的据点建造、制作时，使用其他据点储物箱中的材料，并从来源库存实际扣除。没有固定物品白名单、材料数量或据点数限制。

## 验证范围

2026-10-31 用户实测通过：A 箱子放入 31 石头，背包无石头，B 无箱子、无石头；B 显示可用材料并成功建造；回 A 确认石头按实际成本减少。

其他物品、箱子种类、三个以上据点、进档后未访问的远处据点、制作/生产、材料不足、新建/拆除箱子、重进存档、快速堆叠、物品检索以及不同公会隔离尚未验收。多人客户端、联机主机和专用服务器不属于本次已验证范围；远程客户端显示适配在此构建中未启用。本版不提供专用服务器安装规则。

## 依赖

- Steam Windows 版 Palworld 1.0.5.102999。
- **UE4SS Experimental (Palworld)，2281fa31**，包名 `UE4SSExperimentalPW`；先确认它能在游戏中正常加载。只验证过这一构建，其他 UE4SS 版本的 C++ ABI 兼容性未确认。
- 本包不附带 UE4SS、PalSchema、游戏文件或存档；不依赖 PalSchema。

## 下载文件

- `ResourceShare-3.7.1-local-test2-Palworld-1.0.5-Win64.zip`：普通玩家使用，包含游戏根目录相对路径。
- `ResourceShare-3.7.1-local-test2-ModUploader.zip`：给 Mod Uploader 使用的平铺包，根目录含 `Info.json`。不能直接当游戏根目录覆盖包使用。
- `SHA256SUMS.txt`：Release 附件校验值。

## 手动安装 / 从旧版升级

1. 退出游戏。升级时备份原来的 `Mods/NativeMods/UE4SS/Mods/ziyuan` 目录。
2. 如果订阅过原“资源互通”，先禁用或取消订阅旧包，并完成旧包卸载，再安装本包。两者使用相同包名 `ziyuan`；避免旧 Workshop 包再次安装覆盖本版，也不要同时运行其他 IntegratedStorage 实现。
3. 解压 **Win64.zip**，将其中 `Mods` 文件夹合并到 Palworld 游戏根目录。最终必须存在：
   `Mods/NativeMods/UE4SS/Mods/ziyuan/dlls/main.dll`。
4. 编辑现有 `Mods/NativeMods/UE4SS/Mods/mods.txt`，在 Keybinds 段前添加或确认 **一行** `ziyuan : 1`。不要用其他人的 mods.txt 覆盖自己的文件；本包不附带全局 mods.txt。
5. 完全重启游戏，进入单人存档后等待约 10 秒，再检查建造材料和真实扣料。此构建不得热重载。

包中的 `Scripts/main.lua` 仅输出启动提示，必须与 DLL 一起升级，不能保留原 v2.3 Lua 同步逻辑并行运行。已有 `config.txt` 自定义设置可先备份后恢复。

使用其他 UE4SS 安装布局时，可将 Win64 包内完整的 `ziyuan` 文件夹复制到实际 UE4SS `Mods` 目录；该布局未在本次游戏环境验证。

## Mod Uploader 包

将 ModUploader.zip 解压到 Mod Uploader 创建的模组内容目录，加载根目录 `Info.json`。`Type: Lua` 是 Pocketpair 用于定位 UE4SS Mods 子目录的安装类型，本包功能由其中 `dlls/main.dll` 实现；Targets 同时包括 DLL、脚本、配置和许可证。依赖已声明为 `UE4SSExperimentalPW`。

这个 GitHub Release 没有发布到 Steam Workshop，也没有沿用原包的 Workshop ID。若以后发布到 Workshop，须在自己的新条目中测试官方安装流程；本次只检查包结构与元数据，未执行 Uploader 上传或安装验收。

## 配置与排错

- `verbose = true`：启用有限的启动/扫描诊断。
- `reconcile_interval_ms = 2000`：默认每 2 秒刷新发现与材料计数快照；最小 500。物品显示可能存在约 2 秒刷新延迟。
- 日志：`Mods/NativeMods/UE4SS/UE4SS.log`。
- 正常启动应包含四个原生钩子的 `hooked=true` 和 `3.7.1-local-test2 native hooks installed`；进档后有 `ROLE server=1`、`SRV discover`。
- 出现 `incomplete native resolution` 或 `hook installation rolled back` 表示未成功启用，请报告版本、安装布局、复现步骤和相关 ISGATE 摘录。提交日志前删去个人信息。

卸载：退出游戏，在 mods.txt 将 ziyuan 设为 0 或移除该行，移走 `ziyuan` 文件夹；需要回退旧版时恢复先前备份。通过官方加载器安装的版本应由该加载器卸载，避免遗留记录再次安装。

## 署名、许可证和规范来源

原作者 Sarfflow；1.0.5 上游适配参考 IanMoroney 的 PR #5；本地修复与发布 EBXXIV8319。原中文分发包作者字段为梅川库梓，其原始元数据作为仓库基线保留，不作为本发布包的作者声明或 Workshop 身份。

附带原作者 MIT LICENSE、MinHook/HDE 许可，以及 fmt 与 UE4SS 许可；详见 `NOTICE.md`、`LICENSE`、`MINHOOK-LICENSE.txt` 和 `licenses/`。

- [Pocketpair 安装规则](https://github.com/pocketpairjp/PalworldModUploader/blob/main/PalworldModUploader/docs/en/04-Tech.md)
- [Pocketpair Mod Uploader 与元数据](https://github.com/pocketpairjp/PalworldModUploader/blob/main/PalworldModUploader/docs/en/03-ModUploader.md)
- [UE4SS C++ 模组安装](https://docs.ue4ss.com/dev/guides/installing-a-c%2B%2B-mod.html)
- [源码与问题反馈](https://github.com/EBXXIV8319/Palmod)
