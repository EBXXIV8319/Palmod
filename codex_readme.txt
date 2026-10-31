项目：Palmod

1. 当前修复对象为 resource_share，游戏版本为 Palworld v1.0.5.102999，测试模式为本机单人存档。目标是同公会所有据点使用所有据点储物箱中的全部物品；10 个石头只是示例，不得将物品种类、数量或据点数写死。
2. 先阅读 resource_share/README.md、docs/diagnosis-2026-10-31.md 和 docs/repair-plan.md。
3. initial baseline 提交中的 Scripts/main.lua、Info.json、InstallManifest.json 是游戏目录中原文件的逐字节副本；SHA-256 记录在 baseline.sha256。
4. resource_share 是仓库目录名；实际安装包名仍为 ziyuan。调整名称或安装布局时需同步检查安装规则。
5. 先修改仓库副本。部署测试时备份被替换文件；不得把“加载成功”或 pooled 日志当作功能修复成功。
6. 接口和原生地址必须通过当前版本源码、反射或运行时证据验证，不猜测接口，不直接套用旧版本内存偏移。
7. 保留 Sarfflow 原作者署名与本地分发包元数据；明确区分原始实现与后续修复。
8. 不提交游戏本体、存档、完整运行日志、凭据或构建产物。仅保存必要且经过检查的诊断摘录。
9. 验收同时覆盖材料显示、实际扣料、材料不足、新增/拆除箱子、切换地图和重新进档；记录尚未验证的项目。
10. 使用 Wolfram MCP 时，在交付记录中附上实际运行的 Wolfram 命令。
