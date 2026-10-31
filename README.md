# Palmod

Palworld 模组修复与发行。目标环境：**Palworld v1.0.5.102999，Windows x64，本机单人存档**。

## 资源互通 / Resource Share

同一公会的据点可使用其他据点储物箱中的材料，并从来源箱子实际扣除。实现不限定两个据点、石头或固定数量；使用范围遵守原生配方规则。

**3.7.1-local-test2 预发布版**已通过用户测试：A 有 31 石头，背包无石头，B 无箱子无石头，B 建造成功且 A 正确扣料。其他材料、箱子、更多据点、远处未访问据点及生命周期等场景仍待验收。

- [下载 Release](https://github.com/EBXXIV8319/Palmod/releases/tag/resource-share-v3.7.1-local-test2)：普通玩家选择 Win64.zip，GitHub 自动生成的 Source code 不含 DLL。
- [中文安装、依赖、升级与卸载](resource_share/release/README.zh-CN.md)
- [English installation guide](resource_share/release/README.en.md)
- [源码与排查记录](resource_share/README.md)
- [署名与许可证说明](resource_share/NOTICE.md)

依赖 UE4SS Experimental (Palworld) **2281fa31**；加载器未捆绑。此构建的远程客户端显示适配未启用，联机和专用服务器未验证。

原作者 Sarfflow；上游 1.0.5 适配参考 IanMoroney；本地修复与发布 EBXXIV8319。原始安装包快照保存在 `resource-share-baseline-v2.3` 标签，修复版在 `fix/resource-share-1.0.5` 分支。仓库不包含游戏本体、存档、私有 SDK 或二进制构建缓存；可运行包通过 Release 分发。

开始修改前阅读 [codex_readme.txt](codex_readme.txt)。仓库是开发副本，不会自动修改游戏安装目录。
