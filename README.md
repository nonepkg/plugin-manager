<div align="center">
	<img width="200" src="docs/logo.png" alt="logo"></br>

# Nonebot Plugin Manager

基于 [nonebot2](https://github.com/nonebot/nonebot2) 和 [go-cqhttp](https://github.com/Mrs4s/go-cqhttp) 的**非侵入式**插件管理器

[![License](https://img.shields.io/github/license/Jigsaw111/nonebot_plugin_manager)](LICENSE)
![Python Version](https://img.shields.io/badge/python-3.7.3+-blue.svg)
![NoneBot Version](https://img.shields.io/badge/nonebot-2.0.0a11+-red.svg)
![Pypi Version](https://img.shields.io/pypi/v/nonebot-plugin-manager.svg)

</div>

### 安装

#### 从 PyPI 安装（推荐）

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

#### 从 GitHub 安装（不推荐）

```bash
git clone https://github.com/Jigsaw111/nonebot_plugin_manager.git
```

### 使用

**使用前请先确保命令前缀为空，否则请在以下命令前加上命令前缀 (默认为 `/` )。**

- `npm list` 查看当前会话插件列表
- - `-i, --ignore` 可选参数，显示已忽略的插件
- - `-s, --store` 可选参数，查看插件商店列表（仅超级用户可用）
- - `-gl, --global` 可选参数，管理全局设置（仅超级用户可用）
- - `-g group_id, --group group_id` 可选参数，管理指定群设置（仅超级用户可用）
- - `-u user_id, --user user_id` 可选参数，管理指定用户设置（仅超级用户可用）
- - `-d, --default` 可选参数，管理默认设置（仅超级用户可用）

- `npm block 插件名...` 屏蔽当前会话插件 （仅群管及超级用户可用）
- - `-a, --all` 可选参数，全选插件
- - `-r, --reverse` 可选参数，反选插件
- - `-gl, --global` 可选参数，管理全局设置（仅超级用户可用）
- - `-g group_id, --group group_id` 可选参数，管理指定群设置（仅超级用户可用）
- - `-u user_id, --user user_id` 可选参数，管理指定用户设置（仅超级用户可用）
- - `-d, --default` 可选参数，管理默认设置（仅超级用户可用）

- `npm unblock 插件名...` 启用当前会话插件 （仅群管及超级用户可用）
- - `-a, --all` 可选参数，全选插件
- - `-r, --reverse` 可选参数，反选插件
- - `-gl, --global` 可选参数，管理全局设置（仅超级用户可用）
- - `-g group_id, --group group_id` 可选参数，管理指定群设置（仅超级用户可用）
- - `-u user_id, --user user_id` 可选参数，管理指定用户设置（仅超级用户可用）
- - `-d, --default` 可选参数，管理默认设置（仅超级用户可用）

- `npm info 插件名` 查询插件信息 （仅超级用户可用）

*以下功能尚未实现*

- `npm install 插件名...` 安装插件 （仅超级用户可用）
- - `-i index, --index index` 指定 PyPI 源

- `npm uninstall 插件名...` 卸载插件 （仅超级用户可用）
- - `-a, --all` 可选参数，全选插件

### 导出

```python
from nonebot import require

export = require("nonebot_plugin_manager")

# 启用/禁用插件
export.block_plugin(
    plugins: Iterable[str],
    type: Optional[str] = None,
    user_id: Optional[int] = None,
    group_id: Optional[int] = None,
) -> Dict[str, Optional[bool]]
export.unblock_plugin(
    plugins: Iterable[str],
    type: Optional[str] = None,
    user_id: Optional[int] = None,
    group_id: Optional[int] = None,
) -> Dict[str, Optional[bool]]

# 获取指定会话插件列表
export.get_plugin_list(
    type: Optional[str] = None,
    user_id: Optional[int] = None,
    group_id: Optional[int] = None,
    show_ignore: bool = False,
) -> Dict[str, bool]
```

### Q&A

- **这是什么？**  
  基于 import hook 的插件管理器，能够在不重启 nonebot2 的情况下分群管理插件。
- **有什么用？**  
  在 nonebot2 仍然缺乏插件管理机制的时期暂时充当插件管理器。
- **自造 Rule 不是更好？**  
  Rule 当然更好且更有效率，但是 Rule 是一种**侵入式**的插件管理方式，需要用户自行修改其他插件，这对于管理从 pypi 安装的插件来说相对复杂。而使用本插件，你不需要修改其他插件的任何内容，更符合插件之间**松耦合**的设计原则。

### Thanks

[nonebot/nb-cli](https://github.com/nonebot/nb-cli)

<details>
<summary>展开更多</summary>

### 原理

使用 `run_preprocessor` 装饰器，在 Matcher 运行之前检测其所属的 Plugin 判断是否打断。

事实上 Nonebot 还是加载了插件，所以只能算是**屏蔽**而非**卸载**。

*以下功能尚未实现*

当然，你也可以使用 `npm uninstall` 命令来真正卸载插件，但我不建议你这样做，因为该命令将会重启 Nonebot 。

### To Do

- [x] 分群插件管理
- [ ] 调整优先级为 global > user > group > default
- [ ] 可同时管理多个 群/用户 的插件列表

*咕咕咕*

- [ ] 安装卸载插件

### Bug

- [ ] 无法停用 Matcher 以外的机器人行为（如 APSchedule ）  
      **解决方法：** 暂无
- [x] 任何人都可以屏蔽/启用插件
- [ ] 如果加载了内置插件将会导致错误  
      **解决方法：** 问低调佬

### Changelog

- 210418 0.4.0-alpha.4
- - 新增 `--ignore` 用于显示已忽略的插件（即没有 Matcher 的插件和 npm 本身）
- - 修复判断表达式错误导致的插件列表为空
- - 修复使用 load_from_toml 加载插件时产生的错误
- - 修复 export 的函数名称错误
- - 修复 npm info 指令不响应的错误
- - 修复 global 设置无效的错误
- 210417 0.4.0-alpha.1
- - 配置文件格式更换为 `.yml` 
- - list/block/unblock 新增 `globally` 选项，优先级为 global > user/group > default
- - 重构代码，分离 handle 与 data
- - block/unblock 新增 `--reverse` 选项，可反选插件
- 210415
- - 不再将没有 Matcher 的插件添加到插件列表。
- 210403
- - 分离默认设置与私聊设置，默认设置的键值改为 `default`
- 210402
- - 修复 nonebot 2.0.0a13 更新导致的 bug。
- 210331
- - 添加 logo。
- 210330
- - 修复禁用/启用颠倒的 bug。
- 210329
- - 修复 block/unblock 指令中的 -a 参数无效的 bug，修复文档中导出部分的错误。
- 210320
- - 新增 `get_group_plugin_list` 的 export 用于获取群插件列表。
- 210317
- - 调整项目结构，将绝大多数数据处理操作移至 data，handle 只负责调用；修改 export，不再对其他插件暴露底层接口。
- 210314
- - 修复 `npm list`  的 --group 参数不起作用的 bug
- - 新增 `info` 子命令，用于查询插件信息
- 210313
- - 实现爬取插件商店列表
- - 新增 export 导出给其他插件
- 210312
- - `setting.json` 重命名为 `plugin_list.json`，结构改为 `plugin:{group_id:true,group_id:false}`
- 210310 0.3.0
- - 将__init__.py分离成 setting, command, nb 三个文件
- 210310 0.2.0
-  - Matcher 类型更改为 shell_command
-  - 使用 `setting.json` 作为配置文件，基本结构为 `group_id:{plugin:true,plugin:false}` 
- 210307 0.1.0
- - 上架插件商店
- - 确定了通过 `run_preprocessor` 屏蔽 Matcher 的基本原理
- - 使用 `block_list` 作为全局设置（即只屏蔽 block_list 中的插件）

</details>
