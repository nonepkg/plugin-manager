<div align="center">
  <img width="200" src="https://raw.githubusercontent.com/nonepkg/plugin-manager/master/docs/logo.png" alt="logo"></br>

# Premium Nonebot Plugin Manager

[NoneBot 2](https://github.com/nonebot/nonebot2) 的**非侵入式**插件管理器

[![License](https://img.shields.io/github/license/Jigsaw111/nonebot_plugin_manager)](LICENSE)
![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)
![NoneBot Version](https://img.shields.io/badge/nonebot-2.2.1+-red.svg)
![Pypi Version](https://img.shields.io/pypi/v/nonebot-plugin-manager.svg)

</div>

## 安装

*插件重写中，之前版本的问题不再回复。*

### 从 PyPI 安装（推荐）

- 使用 nb-cli

```bash
nb plugin install nonebot-plugin-manager
```

- 使用 pdm

```bash
pdm add nonebot-plugin-manager
```

### 从 GitHub 安装（不推荐）

```bash
pdm add git+https://github.com/nonepkg/plugin-manager
```

## 使用

### 命令

**使用前请先确保命令前缀为空，否则请在以下命令前加上命令前缀 (默认为`/`)。**

- `npm block/disable <plugin ...>`禁用插件（需要权限）
  - `plugin ...`必选参数，需要禁用的插件名
  - `-a, --all`可选参数，全选插件
  - `-r, --reverse`可选参数，反选插件
  - `-u <user_id ...>, --user <user_id ...>`可选参数，管理指定用户设置（仅超级用户可用）
  - `-g <group_id ...>, --group <group_id ...>`可选参数，管理指定群设置（仅超级用户可用）
  - [ ] `-s|--scope`

- `npm unblock/enable <plugin ...>`启用插件（需要权限）
  - `plugin ...`必选参数，需要禁用的插件名
  - `-a, --all`可选参数，全选插件
  - `-r, --reverse`可选参数，反选插件
  - `-u <user_id ...>, --user <user_id ...>`可选参数，管理指定用户设置（仅超级用户可用）
  - `-g <group_id ...>, --group <group_id ...>`可选参数，管理指定群设置（仅超级用户可用）

- [ ] `npm ban <user ...>`
- [ ] `npm unban <user ...>`
  user :ms.at or platform/id

## 原理

使用`run_preprocessor`装饰器，在 Matcher 运行之前检测其所属的 Plugin 判断是否打断。

事实上 Nonebot 还是加载了插件，所以只能算是**屏蔽**而非**卸载**。

## TODO

- [ ] 新的权限管理
- [ ] 提供自动授予群管理员群内 write 权限的配置项

## 缺陷

- 无法停用 Matcher 以外的机器人行为（如 APScheduler ）
