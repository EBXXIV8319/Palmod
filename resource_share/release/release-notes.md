同一公会跨据点资源互通，面向 **Palworld 1.0.5.102999 / Windows x64 / 本机单人存档**的预发布版。

### 已验证

用户实测：A 箱子放 31 石头、背包无石头、B 无箱子无石头；在 B 材料显示正常且建造成功，A 的石头按实际成本减少。

其他物品/箱子类型、三个以上据点、未访问的远处据点、制作/生产、材料不足、新增/拆箱、重新进档、快速堆叠、物品检索和不同公会隔离尚未验收。联机与专用服务器未验证；远程客户端显示适配未启用。本次仅发布已测试 DLL，没有重编译或更改其运行逻辑。

### 下载与安装

- **普通玩家下载 `ResourceShare-3.7.1-local-test2-Palworld-1.0.5-Win64.zip`**。
- 依赖 **UE4SS Experimental (Palworld) 2281fa31**（`UE4SSExperimentalPW`），未附带加载器；其他 UE4SS 版本未验证。
- 退出游戏、备份旧 ziyuan；先禁用/卸载原 Workshop 资源互通以免覆盖，再把 ZIP 中的 `Mods` 合并到游戏根目录，在现有 `Mods/NativeMods/UE4SS/Mods/mods.txt` 启用一行 `ziyuan : 1`。
- 完全重启并进档等待约 10 秒。详细升级、配置、卸载和排错见包内 `README.zh-CN.md` / `README.en.md`。
- `ResourceShare-3.7.1-local-test2-ModUploader.zip` 是带 Info.json、依赖与完整 Targets 的内容包，不能直接覆盖到游戏根目录。未发布到 Steam Workshop，也未验收 Uploader 安装/上传流程。
- `SHA256SUMS.txt` 校验下载附件；`release-manifest.json` 记录二进制来源、验证范围和包内文件哈希。GitHub 自动生成的 Source code 不包含可运行 DLL。

### 来源

Sarfflow 原作；IanMoroney 的 [PR #5](https://github.com/Sarfflow/palworld-integrated-storage/pull/5) 提供 1.0.5 适配参考；EBXXIV8319 进行本地修复和发行。中文原分发包作者字段为梅川库梓。附带原 MIT 与第三方许可证，保留署名，不沿用原 Workshop 发布身份。

安装布局与元数据参照 [Pocketpair 文档](https://github.com/pocketpairjp/PalworldModUploader/blob/main/PalworldModUploader/docs/en/04-Tech.md) 和 [UE4SS C++ 模组安装文档](https://docs.ue4ss.com/dev/guides/installing-a-c%2B%2B-mod.html)。

**English:** Prerelease for Windows x64, Palworld 1.0.5.102999 and UE4SS 2281fa31, local single-player. Cross-base stone use and correct source consumption were user-verified with an empty destination base; all other cases remain pending. Download the Win64 ZIP for manual installation and follow the included English README. No Steam Workshop upload was performed.
