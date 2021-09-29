# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

## 0.5.1 - 2021-09-25

### Changed

- 交换`chmod`命令的参数位置

### Fixed

- 修复 NPM 能够将自己屏蔽的问题
- 修复任何人都可以屏蔽/启用插件的问题
- 修复`-a --all`参数能够修改不可见插件的问题
- 修复遇到 MessageEvent 之外的其他 Event 时产生的错误

## 0.5.0 - 2021-09-09

### Fixed

- 适配 nonebot2-2.0.0a15

## 0.5.0-alpha.3 - 2021-04-28

### Added

- 新增类 UNIX 权限系统

### Changed

- 命令`list`改为`ls`

### Removed

- 不再保留插件历史记录

## 0.5.0-alpha.2 - 2021-04-23

### Added

- 新增`npm set`命令切换黑/白名单模式

### Changed

- 将 ignore, global 等配置整合成 mode

## 0.5.0-alpha.1 - 2021-04-21

### Added

- 黑/白名单模式切换
- 可一次管理多个群/用户的插件

### Changed

- 调整优先级为 global > user > group

## 0.4.0-alpha.4 - 2021-04-18

### Added

- 新增`--ignore`参数用于显示已忽略的插件（即没有 Matcher 的插件和 npm 本身）

### Fixed

- 修复判断表达式错误导致的插件列表为空
- 修复使用 load_from_toml 加载插件时产生的错误
- 修复 export 的函数名称错误
- 修复 npm info 指令不响应的错误
- 修复 global 设置无效的错误

## 0.4.0-alpha.1 - 2021-04-17

### Added

- list/block/unblock 新增`globally`选项，优先级为 global > user/group > default
- block/unblock 新增`--reverse`选项，可反选插件

### Changed

- 配置文件格式更换为`.yml`
- 重构代码，分离 handle 与 data

## 2021-04-15

- 不再将没有 Matcher 的插件添加到插件列表。

## 2021-04-03

- 分离默认设置与私聊设置，默认设置的键值改为`default`

## 2021-04-02

- 修复 nonebot 2.0.0a13 更新导致的 bug。

## 2021-03-31

- 添加 logo。

## 2021-03-30

- 修复禁用/启用颠倒的 bug。

## 2021-03-29

- 修复 block/unblock 指令中的 -a 参数无效的 bug，修复文档中导出部分的错误。

## 2021-03-20

- 新增`get_group_plugin_list`的 export 用于获取群插件列表。

## 2021-03-17

- 调整项目结构，将绝大多数数据处理操作移至 data，handle 只负责调用；修改 export，不再对其他插件暴露底层接口。

## 2021-03-14

- 修复`npm list` 的 --group 参数不起作用的 bug
- 新增`info`子命令，用于查询插件信息

## 2021-03-13

- 实现爬取插件商店列表
- 新增 export 导出给其他插件

## 2021-03-12

- `setting.json`重命名为`plugin_list.json`，结构改为`{plugin: {group_id: true, group_id: false}}`

## 0.3.0 - 2021-03-10

### Changed

- 将__init__.py 分离成 setting, command, nb 三个文件

## 0.2.0 - 2021-03-10

### Changed

- Matcher 类型更改为 shell_command
- 使用`setting.json`作为配置文件，基本结构为`{group_id: {plugin: true,plugin: false}}`

## 0.1.0 - 2021-03-07

### Added

- 上架插件商店
- 确定了通过`run_preprocessor`屏蔽 Matcher 的原理
- 使用`block_list`作为全局设置（即只屏蔽 block_list 中的插件）
