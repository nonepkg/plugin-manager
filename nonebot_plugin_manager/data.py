import yaml
import httpx
from pathlib import Path
from typing import Any, Iterable, Optional, Dict, List

__DATA_PATH = Path() / "data" / "manager" / "plugin_list.yml"


def get_plugin_info(plugin: str) -> str:
    store_plugin_list = __get_store_plugin_list()
    if plugin in store_plugin_list:
        plugin = store_plugin_list[plugin]
        return (
            f"ID: {plugin['id']}\n"
            f"Name: {plugin['name']}\n"
            f"Description: {plugin['desc']}\n"
            f"Latest Version: {httpx.get('https://pypi.org/pypi/'+plugin['link']+'/json').json()['info']['version']}\n"
            f"Author: {plugin['author']}\n"
            f"Repo: https://github.com/{plugin['repo']}"
        )
    else:
        return "查无此插件！"


def get_plugin_list(
    type: Optional[str] = None,
    user_id: Optional[int] = None,
    group_id: Optional[int] = None,
) -> Dict[str, bool]:

    plugin_list = __load_plugin_list()
    tmp_plugin_list = {}

    for plugin in plugin_list:

        if "global" in plugin_list[plugin]:
            tmp_plugin_list[plugin] = plugin_list[plugin]["global"]

        if type == "user" or user_id in plugin_list[plugin]["user"]:
            tmp_plugin_list[plugin] = plugin_list[plugin]["user"][user_id]

        if type == "group" or group_id in plugin_list[plugin]["group"]:
            tmp_plugin_list[plugin] = plugin_list[plugin]["group"][group_id]

        if type == "default" or plugin not in tmp_plugin_list:
            tmp_plugin_list[plugin] = plugin_list[plugin]["default"]

    return tmp_plugin_list


def get_store_pulgin_list() -> str:
    message = "商店插件列表如下："
    for plugin in __get_store_plugin_list():
        if plugin in __load_plugin_list() or plugin == "nonebot_plugin_manager":
            message += f"\n[o] {plugin}"
        else:
            message += f"\n[x] {plugin}"
    return message


def auto_update_plugin_list(loaded_plugin_list: List[str]):
    plugin_list = __load_plugin_list()
    for plugin in loaded_plugin_list:
        if plugin not in plugin_list:
            plugin_list[plugin] = {"default": True, "user": {}, "group": {}}
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


# 获取商店插件列表
def __get_store_plugin_list() -> dict:
    store_plugin_list = {}
    for plugin in httpx.get(
        "https://cdn.jsdelivr.net/gh/nonebot/nonebot2@master/docs/.vuepress/public/plugins.json"
    ).json():
        store_plugin_list.update({plugin["id"]: plugin})
    return store_plugin_list


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
        if plugin in plugin_list:

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
                "global" not in plugin_list[plugin]
                or plugin_list[plugin]["global"] == block
            ) and (status is None or status == block):
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
