import httpx
from typing import Dict

from .data import get_plugin_list


# 获取商店插件列表
def __get_store_plugin_list() -> dict:
    store_plugin_list = {}
    for plugin in httpx.get(
        "https://cdn.jsdelivr.net/gh/nonebot/nonebot2@master/docs/.vuepress/public/plugins.json"
    ).json():
        store_plugin_list.update({plugin["id"]: plugin})
    return store_plugin_list


def get_store_pulgin_list() -> Dict[str, bool]:
    plugin_list = get_plugin_list(show_ignore=True)
    tmp_plugin_list = {}
    for plugin in __get_store_plugin_list():
        if plugin in plugin_list:
            tmp_plugin_list[plugin] = True
        else:
            tmp_plugin_list[plugin] = False
    return tmp_plugin_list


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
