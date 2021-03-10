# Nonebot Plugin Manager

*适用于 [nonebot2](https://github.com/nonebot/nonebot2) 以及 [go-cqhttp](https://github.com/Mrs4s/go-cqhttp) 的插件管理器*

[![License](https://img.shields.io/github/license/Jigsaw111/nonebot_plugin_manager)](LICENSE)
![Python Version](https://img.shields.io/badge/python-3.7.3+-blue.svg)
![NoneBot Version](https://img.shields.io/badge/nonebot-2.0.0a11+-red.svg)
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

**使用前请先确保命令前缀设置为空，否则请在以下命令前加上自己的命令前缀 (默认为 `/` )。**

`npm list` 查看插件列表

`npm block 插件名...` 屏蔽插件

`npm unblock 插件名...` 启用插件

`-a,--a` 可选参数，全选插件

`-d,--d` 可选参数，全局管理

### TO DO

- [x] 分群插件管理
- [ ] 调用 nb-cli 安装卸载插件

<details>
<summary>展开更多</summary>

### 原理

使用 `run_preprocessor` 装饰器，在 Matcher 运行之前检测其所属的 Plugin 判断是否打断。

事实上 Nonebot 还是加载了插件，所以只能算是**屏蔽**而非**卸载**。

### Bug

- [ ] 无法停用 Matcher 以外的功能（也就是说无法屏蔽主动发消息的插件，例如 Harukabot ）。
- [x] 目前任何人都可以管理插件

</details>