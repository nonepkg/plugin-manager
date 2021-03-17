import httpx

from ._pip import _call_pip_install, _call_pip_update, _call_pip_uninstall


def get_store_plugin_list() -> dict:
    store_plugin_list = {}
    for plugin in httpx.get(
        "https://cdn.jsdelivr.net/gh/nonebot/nonebot2@master/docs/.vuepress/public/plugins.json"
    ).json():
        store_plugin_list.update({plugin["id"]: plugin})
    return store_plugin_list


def get_plugin_info(plugin: str):
    store_plugin_list = get_store_plugin_list()
    if plugin in store_plugin_list:
        plugin = store_plugin_list[plugin]
        return (
            f"ID: {plugin['id']}\n"
            f"Name: {plugin['name']}\n"
            f"Description: {plugin['desc']}\n"
            f"Version: {httpx.get('https://pypi.org/pypi/'+plugin['link']+'/json').json()['info']['version']}\n"
            f"Author: {plugin['author']}\n"
            f"Repo: https://github.com/{plugin['repo']}"
        )
    else:
        return "查无此插件！"
