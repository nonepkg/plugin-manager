# Nonebot Plugin Manager

适用于 [nonebot2](https://github.com/nonebot/nonebot2) 的**非侵入式**插件管理器

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

### 使用

**使用前请先确保命令前缀为空，否则请在以下命令前加上命令前缀 (默认为 `/` )。**

`npm list` 查看插件列表

`npm block 插件名...` 屏蔽插件 （仅群管及超级用户可用）

`npm unblock 插件名...` 启用插件 （仅群管及超级用户可用）

`-a, --all` 可选参数，全选插件 （仅群管及超级用户可用）

`-d, --default` 可选参数，管理默认设置 （仅超级用户可用）

`-g group_id, --group group_id` 可选参数，管理群设置（仅超级用户可用）

### Q&A

- **这是什么？**  
  基于 import hook 的插件管理器，能够在不重启 nonebot2 的情况下分群管理插件。
- **有什么用？**  
  在 nonebot2 仍然缺乏插件管理机制的时期暂时充当插件管理器。
- **自造 Rule 不是更好？**  
  Rule 当然更好且更有效率，但是 Rule 是一种**侵入式**的插件管理方式，需要用户自行修改其他插件，这对于管理从 pypi 安装的插件来说相对复杂。而使用本插件，你不需要修改其他插件的任何内容，更符合插件之间**松耦合**的设计原则。

<details>
<summary>展开更多</summary>

### 原理

使用 `run_preprocessor` 装饰器，在 Matcher 运行之前检测其所属的 Plugin 判断是否打断。

事实上 Nonebot 还是加载了插件，所以只能算是**屏蔽**而非**卸载**。

### TO DO

- [x] 分群插件管理
- [ ] 安装卸载插件

### Bug

- [ ] 无法停用 Matcher 以外的功能（也就是说无法屏蔽主动发消息的插件，例如 Harukabot ）。
- [x] 目前任何人都可以屏蔽/启用插件

</details>