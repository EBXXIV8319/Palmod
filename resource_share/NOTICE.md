# 署名与来源 / Attribution

当前原生修复基于 **Sarfflow** 的 IntegratedStorage C++ 实现，以及 **IanMoroney** 的 Palworld 1.0.5 [适配 PR #5](https://github.com/Sarfflow/palworld-integrated-storage/pull/5)，参考提交 `6a3de750da7d416a2b02d1852c3dac27d21a6b8b`。

**EBXXIV8319** 进行本地 UE4SS 兼容构建、接口查找修正、线程和生命周期适配、属性反射改造以及发行整理。这是派生修复版，不代表原作者官方发布。

原 C++ MIT 版权声明及许可证完整保存在 `native/reference/LICENSE`，发行包使用同一内容作为 `LICENSE`。MinHook/HDE 使用其 BSD 风格许可证，见 `native/MINHOOK-LICENSE.txt`（发行包中为 `MINHOOK-LICENSE.txt`）。发行包还附带 `licenses/FMT-LICENSE.txt` 和 `licenses/UE4SS-LICENSE.txt`，分别保留 fmt 与 UE4SS 公共接口相关代码的许可。加载器、私有 Unreal SDK 源码和游戏文件均不在发行包中。

原始 Lua 为 IntegratedStorage v2.3，作者 Sarfflow，已在 Git 标签 `resource-share-baseline-v2.3` 保留。原 Lua 包未附 LICENSE；本仓库没有给它重新指定许可证，当前发行包只携带替代它的启动提示脚本。

仓库根源快照中的 `Info.json`、`InstallManifest.json` 来自本地中文“资源互通”分发包：包名 `ziyuan`，作者字段“梅川库梓”，Workshop ID `3763145359`。这些历史元数据保留在基线中；本 GitHub 发行不使用其 Workshop ID，也不冒用该分发包的发布身份。发布用元数据位于 `release/Info.json`，其作者字段区分原作、上游适配和本地维护者。

Original C++: Sarfflow, MIT. Upstream 1.0.5 adaptation: IanMoroney. Local repair and release: EBXXIV8319. Original Chinese package credited 梅川库梓. Preserve all included license notices when redistributing.
