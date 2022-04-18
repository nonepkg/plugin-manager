<div align="center">
	<img width="200" src="docs/logo.png" alt="logo"></br>

# Nonebot Plugin Manager

基于 [nonebot2](https://github.com/nonebot/nonebot2) 和 [go-cqhttp](https://github.com/Mrs4s/go-cqhttp) 的**非侵入式**插件管理器

[![License](https://img.shields.io/github/license/Jigsaw111/nonebot_plugin_manager)](LICENSE)
![Python Version](https://img.shields.io/badge/python-3.7.3+-blue.svg)
![NoneBot Version](https://img.shields.io/badge/nonebot-2.0.0a11+-red.svg)
![Pypi Version](https://img.shields.io/pypi/v/nonebot-plugin-manager.svg)

</div>

## 安装

**插件仍在~~快速~~开发中，遇到问题还请务必提 issue。**

### 从 PyPI 安装（推荐）

- 使用 nb-cli  

```bash
nb plugin install nonebot_plugin_manager
```

- 使用 poetry

```bash
poetry add nonebot_plugin_manager
```

- 使用 pip

```bash
pip install nonebot_plugin_manager
```

### 从 GitHub 安装（不推荐）

```bash
git clone https://github.com/Jigsaw111/nonebot_plugin_manager.git
```

## 使用

### 权限

权限与 UNIX 的权限类似，分为三种用户：超级用户、用户、群。

每种用户包含读、写、执行 3 个权限，分别对应数字 4、2、1，将 3 个权限对应的数字累加，最终得到的值即可作为每种用户所具有的权限。

关于会话中使用什么模式，可参照下表：

| 仅供参考 | 私聊读   | 群聊读 | 私聊写   | 群聊写    | 私聊执行 | 群聊执行  |
| -------- | -------- | ------ | -------- | --------- | -------- | --------- |
| 超级用户 | 超级用户 | 群     | 超级用户 | 超级用户  | 超级用户 | 群        |
| 用户     | 用户     | 群     | 用户     | 无权限    | 用户     | 用户 & 群 |
| 群管理员 | 不存在   | 群     | 不存在   | 用户 & 群 | 不存在   | 用户 & 群 |

包含 Matcher 的插件默认权限为`755`，不含 Matcher 的插件默认权限为`311`。

> 例：`npm chmod nonebot_plugin_nodice 757`命令可将 nonebot_plugin_nodice 的权限设置为`757`
> 即超级用户可写可读可执行，用户可读可执行，群可写可读可执行。

只有超级用户可以修改插件的权限，可以使用绝对模式（八进制数字模式）~~，符号模式~~指定文件的权限。

### 命令

**使用前请先确保命令前缀为空，否则请在以下命令前加上命令前缀 (默认为`/`)。**

- `npm ls`查看当前会话插件列表
- - `-s, --store`互斥参数，查看插件商店列表（仅超级用户可用）
- - `-u user_id, --user user_id`互斥参数，查看指定用户插件列表（仅超级用户可用）
- - `-g group_id, --group group_id`互斥参数，查看指定群插件列表（仅超级用户可用）
- - `-a, --all`可选参数，查看所有插件（包括不含 Matcher 的插件）

- `npm info 插件名`查询插件信息 （仅超级用户可用）

- `npm chmod mode plugin ...`设置插件权限（仅超级用户可用）
- - `mode`必选参数，需要设置的权限，参考上文
- - `plugin...`必选参数，需要设置的插件名
- - `-a, --all`可选参数，全选插件
- - `-r, --reverse`可选参数，反选插件

- `npm block plugin...`禁用当前会话插件（需要权限）
- - `plugin...`必选参数，需要禁用的插件名
- - `-a, --all`可选参数，全选插件
- - `-r, --reverse`可选参数，反选插件
- - `-u user_id ..., --user user_id ...`可选参数，管理指定用户设置（仅超级用户可用）
- - `-g group_id ..., --group group_id ...`可选参数，管理指定群设置（仅超级用户可用）

- `npm unblock plugin...`启用当前会话插件（需要权限）
- - `plugin...`必选参数，需要禁用的插件名
- - `-a, --all`可选参数，全选插件
- - `-r, --reverse`可选参数，反选插件
- - `-u user_id ..., --user user_id ...`可选参数，管理指定用户设置（仅超级用户可用）
- - `-g group_id ..., --group group_id ...`可选参数，管理指定群设置（仅超级用户可用）

<!-- TODO

- `npm install plugin...`安装插件（仅超级用户可用）
- - `-i index, --index index`指定 PyPI 源

- `npm uninstall plugin...`卸载插件（仅超级用户可用）
- - `-a, --all`可选参数，全选插件

-->

## Q&A

- **这是什么？**  
  基于 import hook 的插件管理器，能够在不重启 NoneBot2 的情况下分群管理插件。
- **有什么用？**  
  在 NoneBot2 仍然缺乏插件管理机制的时期暂时充当插件管理器。
- **自造 Rule 不是更好？**  
  Rule 当然更好且更有效率，但是 Rule 是一种**侵入式**的插件管理方式，需要用户自行修改其他插件的源码，这对于管理从 PyPI 安装的插件来说相对复杂。而使用本插件，你不需要修改其他插件的任何内容，更符合插件之间**松耦合**的设计原则。

<details>
<summary>展开更多</summary>

## 原理

使用`run_preprocessor`装饰器，在 Matcher 运行之前检测其所属的 Plugin 判断是否打断。

事实上 Nonebot 还是加载了插件，所以只能算是**屏蔽**而非**卸载**。

<!-- TODO

当然，你也可以使用`npm uninstall`命令来真正卸载插件，但我不建议你这样做，因为该命令将会重启 Nonebot 。

-->

## To Do

- [x] 分群插件管理
- [ ] 完善权限系统
- [ ] 设置插件别名

*咕咕咕*

- [ ] 安装卸载插件

## Bug

- [ ] 无法停用 Matcher 以外的机器人行为（如 APScheduler ）  
  **解决方法：** 暂无
- [x] 任何人都可以屏蔽/启用插件
- [x] 如果加载了内置插件将会导致错误

</details>
