# Plugin Manager

*适用于 [nonebot2](https://github.com/nonebot/nonebot2) 以及 [go-cqhttp](https://github.com/Mrs4s/go-cqhttp) 的插件管理器*

[![License](https://img.shields.io/github/license/Jigsaw111/nonebot_plugin_manager)](LICENSE)
![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)
![NoneBot Version](https://img.shields.io/badge/nonebot-2+-red.svg)
![Pypi Version](https://img.shields.io/pypi/v/nonebot-plugin-manager.svg)

### 安装

* 使用nb-cli（推荐）  

```bash
nb plugin install nonebot_plugin_manager
```

* 使用poetry

```bash
poetry add nonebot_plugin_manager
```

### 开始使用

`.plugin list` 查看插件列表

`.plugin block 插件名` 屏蔽插件

`.plugin unblock 插件名` 启用插件

### TO DO

- [ ] 分群插件管理

<details>
<summary>展开更多</summary>

### 原理

使用 `run_preprocessor` 装饰器，在 Matcher 运行之前检测其所属的 Plugin 判断是否打断。

事实上 Nonebot 还是加载了插件，所以只能算是**屏蔽**而非**卸载**。

### Bug

- 无法停用 Matcher 以外的功能。

</details>