import yaml
from pathlib import Path
from typing import Any, Dict, Iterable, Optional

__DATA_PATH = Path() / "data" / "manager" / "plugin_list.yml"


def get_plugin_list(
    type: Optional[str] = None,
    user_id: Optional[int] = None,
    group_id: Optional[int] = None,
    show_ignore: bool = False,
) -> Dict[str, bool]:

    plugin_list = __load_plugin_list()
    tmp_plugin_list = {}

    for plugin in plugin_list:
        if (
            show_ignore
            and plugin_list[plugin]["ignore"] is not None
            or plugin_list[plugin]["ignore"] == False
        ):
            if "global" in plugin_list[plugin]:
                tmp_plugin_list[plugin] = plugin_list[plugin]["global"]
            elif type == "user" or user_id in plugin_list[plugin]["user"]:
                tmp_plugin_list[plugin] = plugin_list[plugin]["user"][user_id]
            elif type == "group" or group_id in plugin_list[plugin]["group"]:
                tmp_plugin_list[plugin] = plugin_list[plugin]["group"][group_id]
            elif type == "default" or plugin not in tmp_plugin_list:
                tmp_plugin_list[plugin] = plugin_list[plugin]["default"]

    return tmp_plugin_list


def auto_update_plugin_list(loaded_plugin_list: Dict[str, bool]):
    plugin_list = __load_plugin_list()

    for plugin in loaded_plugin_list:
        if plugin not in plugin_list:
            plugin_list[plugin] = {"default": True, "user": {}, "group": {}}
        plugin_list[plugin]["ignore"] = not loaded_plugin_list[plugin]

    for plugin in plugin_list:
        if plugin not in loaded_plugin_list:
            plugin_list[plugin]["ignore"] = None

    __dump_plugin_list(plugin_list)


def block_plugin(
    plugins: Iterable[str],
    type: Optional[str] = None,
    user_id: Optional[int] = None,
    group_id: Optional[int] = None,
) -> Dict[str, Optional[bool]]:
    return __update_plugin_list(plugins, True, type, user_id, group_id)


def unblock_plugin(
    plugins: Iterable[str],
    type: Optional[str] = None,
    user_id: Optional[int] = None,
    group_id: Optional[int] = None,
) -> Dict[str, Optional[bool]]:
    return __update_plugin_list(plugins, False, type, user_id, group_id)


# 更新插件列表
def __update_plugin_list(
    plugins: Iterable[str],
    block: bool,
    type: Optional[str] = None,
    user_id: Optional[int] = None,
    group_id: Optional[int] = None,
) -> Dict[str, Optional[bool]]:

    plugin_list = __load_plugin_list()

    result = {}

    for plugin in plugins:
        if plugin in plugin_list and plugin_list[plugin]["ignore"] == False:

            if (
                type == "global"
                and "global" in plugin_list[plugin]
                or type == "default"
            ):
                status = plugin_list[plugin][type]
            elif type == "user" or user_id in plugin_list[plugin]["user"]:
                status = plugin_list[plugin]["user"][user_id]
            elif type == "group" or group_id in plugin_list[plugin]["group"]:
                status = plugin_list[plugin]["group"][group_id]
            else:
                status = None

            if (
                type == "global"
                or "global" not in plugin_list[plugin]
                or plugin_list[plugin]["global"] != block
            ):
                status = not block
                result[plugin] = True
            else:
                result[plugin] = False

            if status is not None:
                if type == "global" or type == "default":
                    plugin_list[plugin][type] = status
                elif type == "user" or user_id:
                    plugin_list[plugin]["user"][user_id] = status
                elif type == "group" or group_id:
                    plugin_list[plugin]["group"][group_id] = status
        else:
            result[plugin] = None

    __dump_plugin_list(plugin_list)

    return result


# 加载插件列表
def __load_plugin_list() -> Dict[str, Any]:
    try:
        return yaml.safe_load(__DATA_PATH.open("r", encoding="utf-8"))
    except FileNotFoundError:
        return {}


# 保存插件列表
def __dump_plugin_list(plugin_list: Dict[str, Any]):
    __DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    yaml.dump(
        plugin_list,
        __DATA_PATH.open("w", encoding="utf-8"),
        allow_unicode=True,
    )
