import httpx

from ._pip import _call_pip_install, _call_pip_update, _call_pip_uninstall


def get_store_plugin_list() -> dict:
    store_plugin_list={}
    for plugin in httpx.get(
        "https://cdn.jsdelivr.net/gh/nonebot/nonebot2@master/docs/.vuepress/public/plugins.json"
    ).json():
        store_plugin_list.update({plugin["id"]:plugin})
    return store_plugin_list