import json
from pathlib import Path

_DATA_PATH = Path() / "data" / "manager" / "plugin_list.json"

# 更新插件列表
def update(plugin_list: dict, loaded_plugin_list: list, keep_history: bool = False):
    for plugin in loaded_plugin_list:
        if plugin not in plugin_list:
            plugin_list[plugin] = {"0": True}
    if not keep_history:
        plugin_list = {
            key: plugin_list[key] for key in plugin_list if key in loaded_plugin_list
        }
    dump(plugin_list)
    return plugin_list


# 加载插件列表
def load() -> dict:
    try:
        return json.load(_DATA_PATH.open("r", encoding="utf-8"))
    except FileNotFoundError:
        return {}


# 保存插件列表
def dump(plugin_list: dict):
    _DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    json.dump(
        plugin_list,
        _DATA_PATH.open("w", encoding="utf-8"),
        indent=4,
        separators=(",", ": "),
    )
