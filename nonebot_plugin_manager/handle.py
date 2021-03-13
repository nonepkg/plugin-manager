from argparse import Namespace

from . import data
from .plugin import _get_plugins


def handle_list(
    args: Namespace,
    plugin_list: dict,
    group_id: str,
    is_admin: bool,
    is_superuser: bool,
) -> str:
    message = ""

    if args.store:
        if is_superuser:
            message += "商店插件列表如下："
            store_plugin_list = _get_plugins()
            for i in range(len(store_plugin_list)):
                if store_plugin_list[i]["id"] in plugin_list:
                    message += f'\n[o] {store_plugin_list[i]["id"]}'
                else:
                    message += f'\n[x] {store_plugin_list[i]["id"]}'
            return message
        else:
            return "获取商店插件列表需要超级用户权限！"

    if args.default:
        if is_superuser:
            group_id = 0
            message += "默认"
        else:
            return "获取默认插件列表需要超级用户权限！"

    if args.group:
        if is_superuser:
            group_id = args.group
            message += f"群{args.group}"
        else:
            return "获取指定群插件列表需要超级用户权限！"

    message += "插件列表如下："
    for plugin in plugin_list:
        if group_id in plugin_list[plugin]:
            message += f'\n[{"o" if plugin_list[plugin][group_id] else "x"}] {plugin}'
        else:
            message += f'\n[{"o" if plugin_list[plugin]["0"] else "x"}] {plugin}'
    return message


def handle_block(
    args: Namespace,
    plugin_list: dict,
    group_id: str,
    is_admin: bool,
    is_superuser: bool,
) -> str:

    if not is_admin and not is_superuser:
        return "管理插件需要群管理员权限！"

    message = ""

    if args.default:
        if is_superuser:
            group_id = 0
            message += "默认"
        else:
            return "管理默认插件需要超级用户权限！"

    if args.group:
        if is_superuser:
            group_id = args.group
            message += f"群{args.group}"
        else:
            return "管理指定群插件需要超级用户权限！"

    message += "结果如下："
    for plugin in args.plugins if not args.all else plugin_list:
        message += "\n"
        if plugin in plugin_list:
            if not group_id in plugin_list[plugin] or plugin_list[plugin][group_id]:
                plugin_list[plugin][group_id] = False
                message += f"插件{plugin}屏蔽成功！"
            else:
                message += f"插件{plugin}已经屏蔽！"
        else:
            message += f"插件{plugin}不存在！"
    data.dump(plugin_list)
    return message


def handle_unblock(
    args: Namespace,
    plugin_list: dict,
    group_id: str,
    is_admin: bool,
    is_superuser: bool,
) -> str:
    message = ""

    if not is_admin and not is_superuser:
        return "管理插件需要群管理员权限！"

    if args.default:
        if is_superuser:
            group_id = 0
            message += "默认"
        else:
            return "管理默认插件需要超级用户权限！"

    if args.group:
        if is_superuser:
            group_id = args.group
            message += f"群{args.group}"
        else:
            return "管理指定群插件需要超级用户权限！"

    message += "结果如下："
    for plugin in args.plugins if not args.all else plugin_list:
        message += "\n"
        if plugin in plugin_list:
            if not group_id in plugin_list[plugin] or not plugin_list[plugin][group_id]:
                plugin_list[plugin][group_id] = True
                message += f"插件{plugin}启用成功！"
            else:
                message += f"插件{plugin}已经启用！"
        else:
            message += f"插件{plugin}不存在！"
    data.dump(plugin_list)
    return message


def handle_install(
    args: Namespace,
    plugin_list: dict,
    group_id: str,
    is_admin: bool,
    is_superuser: bool,
) -> str:
    pass


def handle_update(
    args: Namespace,
    plugin_list: dict,
    group_id: str,
    is_admin: bool,
    is_superuser: bool,
) -> str:
    pass


def handle_uninstall(
    args: Namespace,
    plugin_list: dict,
    group_id: str,
    is_admin: bool,
    is_superuser: bool,
) -> str:
    pass
