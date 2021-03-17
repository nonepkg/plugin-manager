import json
from pathlib import Path

_DATA_PATH = Path() / "data" / "manager" / "plugin_list.json"


def plugin_list(group_id):
    plugin_list = _load_plugin_list()
    message = "插件列表如下："
    for plugin in plugin_list:
        if group_id in plugin_list[plugin]:
            message += f'\n[{"o" if plugin_list[plugin][group_id] else "x"}] {plugin}'
        else:
            message += f'\n[{"o" if plugin_list[plugin]["0"] else "x"}] {plugin}'
    return message


def store_pulgin_list(store_plugin_list):
    message = "商店插件列表如下："
    for plugin in store_plugin_list:
        if plugin in _load_plugin_list() or plugin == "nonebot_plugin_manager":
            message += f"\n[o] {plugin}"
        else:
            message += f"\n[x] {plugin}"
    return message


def auto_update_plugin_list(loaded_plugin_list: list, keep_history: bool = False):
    plugin_list = _load_plugin_list()
    for plugin in loaded_plugin_list:
        if plugin not in plugin_list:
            plugin_list[plugin] = {"0": True}
    if not keep_history:
        plugin_list = {
            key: plugin_list[key] for key in plugin_list if key in loaded_plugin_list
        }
    _dump_plugin_list(plugin_list)
    return plugin_list


def block_plugin(group_id: str, *plugins: str):
    return _update_plugin_list(group_id, True, *plugins)


def unblock_plugin(group_id: str, *plugins: str):
    return _update_plugin_list(group_id, False, *plugins)


# 更新插件列表
def _update_plugin_list(group_id: str, block: bool, *plugins: str):
    plugin_list = _load_plugin_list()
    message = "结果如下："
    operate = "屏蔽" if block else "启用"
    for plugin in plugins:
        message += "\n"
        if plugin in plugin_list:
            if (
                not group_id in plugin_list[plugin]
                or plugin_list[plugin][group_id] == block
            ):
                plugin_list[plugin][group_id] = not block
                message += f"插件{plugin}{operate}成功！"
            else:
                message += f"插件{plugin}已经{operate}！"
        else:
            message += f"插件{plugin}不存在！"
    _dump_plugin_list(plugin_list)
    return message


# 加载插件列表
def _load_plugin_list() -> dict:
    try:
        return json.load(_DATA_PATH.open("r", encoding="utf-8"))
    except FileNotFoundError:
        return {}


# 保存插件列表
def _dump_plugin_list(plugin_list: dict):
    _DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    json.dump(
        plugin_list,
        _DATA_PATH.open("w", encoding="utf-8"),
        indent=4,
        separators=(",", ": "),
    )
