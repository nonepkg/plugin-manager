from argparse import Namespace

from .setting import load_setting, update_setting


def command_list(
    args: Namespace,
    plugin_list: list,
    group_id: int,
    is_admin: bool,
    is_superuser: bool,
) -> str:
    message = ""

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

    default_setting = load_setting(0)
    setting = load_setting(group_id)
    message += "插件列表如下："
    for plugin in plugin_list:
        if setting is not None and plugin in setting:
            message += f'\n[{"o" if setting[plugin] else "x"}] {plugin}'
        else:
            message += f'\n[{"o" if default_setting[plugin] else "x"}] {plugin}'
    return message


def command_block(
    args: Namespace,
    plugin_list: list,
    group_id: int,
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

    setting = load_setting(group_id)
    message += "结果如下："
    for plugin in args.plugins if not args.all else plugin_list:
        message += "\n"
        if plugin in plugin_list:
            if not plugin in setting or setting[plugin]:
                setting[plugin] = False
                message += f"插件{plugin}屏蔽成功！"
            else:
                message += f"插件{plugin}已经屏蔽！"
        else:
            message += f"插件{plugin}不存在！"
    update_setting(group_id, setting)
    return message


def command_unblock(
    args: Namespace,
    plugin_list: list,
    group_id: int,
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

    setting = load_setting(group_id)
    message += "结果如下："
    for plugin in args.plugins if not args.all else plugin_list:
        message += "\n"
        if plugin in plugin_list:
            if not plugin in setting or not setting[plugin]:
                setting[plugin] = True
                message += f"插件{plugin}启用成功！"
            else:
                message += f"插件{plugin}已经启用！"
        else:
            message += f"插件{plugin}不存在！"
    update_setting(group_id, setting)
    return message
