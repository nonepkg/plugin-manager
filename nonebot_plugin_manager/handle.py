from argparse import Namespace

from .plugin import *


def handle_list(args: Namespace) -> str:

    message = ""

    if args.globally:
        if args.is_superuser:
            args.type = "global"
            message = "全局"
        else:
            return "获取全局插件列表需要超级用户权限！"
    elif args.user:
        if args.is_superuser:
            args.type = "user"
            args.user_id = args.user
            message = f"用户 {args.user}"
        else:
            return "获取指定用户插件列表需要超级用户权限！"
    elif args.group:
        if args.is_superuser:
            args.type = "group"
            args.group_id = args.group
            message = f"群 {args.group}"
        else:
            return "获取指定群插件列表需要超级用户权限！"

    if args.ignore:
        if args.is_superuser:
            args.type = "ignore"
        else:
            return "查看已忽略插件需要超级用户权限！"

    if args.store:
        if args.is_superuser:
            message = "默认"
            plugin_list = get_store_pulgin_list()
        else:
            return "获取商店插件列表需要超级用户权限！"
    else:
        message += "插件列表如下：\n"
        plugin_list = PluginList().get_plugin(args.type, args.user_id, args.group_id)

    message += "\n".join(
        f"[{'o' if plugin_list[plugin] else 'x'}] {plugin}" for plugin in plugin_list
    )

    return message


def handle_block(args: Namespace) -> str:

    message = ""
    conv = {}

    plugin_list = PluginList()

    if args.is_admin and not args.is_superuser:
        if args.group_id:
            return "管理群插件需要群管理员权限！"
        else:
            return "管理用户插件需要超级用户权限！"

    if args.globally:
        if args.is_superuser:
            conv["global"] = []
        else:
            return "管理全局插件需要超级用户权限！"
    elif args.user:
        if args.is_superuser:
            conv["user"] = args.user
        else:
            return "管理指定用户插件需要超级用户权限！"
    elif args.group:
        if args.is_superuser:
            conv["group"] = args.group
        else:
            return "管理指定群插件需要超级用户权限！"
    else:
        conv = {
            "user"
            if args.user_id
            else "group": [args.user_id if args.user_id else args.group_id]
        }

    if args.all:
        args.plugins = [
            plugin
            for plugin in plugin_list.get_plugin(args.type, args.user_id, args.group_id)
        ]

    if args.reverse:
        args.plugins = list(
            filter(
                lambda plugin: plugin not in args.plugins,
                plugin_list.get_plugin(args.type, args.user_id, args.group_id),
            )
        )
    result = {}
    for type in conv:
        message += "全局," if type == "group" else "用户 " if type == "user" else "群 "
        for id in conv[type]:
            message += f"{str(id)},"
            result = plugin_list.block_plugin(
                args.plugins,
                type,
                id if type == "user" else None,
                id if type == "group" else None,
            )
    if result:
        message += "中操作结果如下："
        for plugin in result:
            message += "\n"
            if result[plugin]:
                message += f"插件 {plugin} 禁用成功！"
            else:
                message += f"插件 {plugin} 不存在或处于白名单模式！"

    return message


def handle_unblock(args: Namespace) -> str:

    message = ""
    conv = {}
    plugin_list = PluginList()

    if args.is_admin and not args.is_superuser:
        if args.group_id:
            return "管理群插件需要群管理员权限！"
        else:
            return "管理用户插件需要超级用户权限！"

    if args.globally:
        if args.is_superuser:
            conv["global"] = []
        else:
            return "管理全局插件需要超级用户权限！"
    elif args.user:
        if args.is_superuser:
            conv["user"] = args.user
        else:
            return "管理指定用户插件需要超级用户权限！"
    elif args.group:
        if args.is_superuser:
            conv["group"] = args.group
        else:
            return "管理指定群插件需要超级用户权限！"
    else:
        conv = {
            "user"
            if args.user_id
            else "group": [args.user_id if args.user_id else args.group_id]
        }

    if args.all:
        args.plugins = [
            plugin
            for plugin in plugin_list.get_plugin(args.type, args.user_id, args.group_id)
        ]

    if args.reverse:
        args.plugins = list(
            filter(
                lambda plugin: plugin not in args.plugins,
                plugin_list.get_plugin(args.type, args.user_id, args.group_id),
            )
        )
    result = {}
    for type in conv:
        message += "全局," if type == "group" else "用户 " if type == "user" else "群 "
        for id in conv[type]:
            message += str(id)
            result = plugin_list.unblock_plugin(
                args.plugins,
                type,
                id if type == "user" else None,
                id if type == "group" else None,
            )
    if result:
        message += "中操作结果如下："
        for plugin in result:
            message += "\n"
            if result[plugin]:
                message += f"插件 {plugin} 解禁成功！"
            else:
                message += f"插件 {plugin} 不存在或处于白名单模式！"

    return message


def handle_info(args: Namespace) -> str:

    if not args.is_admin and not args.is_superuser:
        return "获取插件信息需要超级用户权限！"

    return get_plugin_info(args.plugin)


def handle_install(args: Namespace) -> str:
    pass


def handle_uninstall(args: Namespace) -> str:
    pass
