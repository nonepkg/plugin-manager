from argparse import Namespace

from .data import *


def handle_list(args: Namespace) -> Namespace:

    if args.store:
        if args.is_superuser:
            args.message = get_store_pulgin_list()
        else:
            args.message = "获取商店插件列表需要超级用户权限！"
    elif args.globally:
        if args.is_superuser:
            args.type = "global"
            args.message += "全局"
        else:
            args.message = "获取全局插件列表需要超级用户权限！"
    elif args.user:
        if args.is_superuser:
            args.user_id = args.user
            args.message += f"用户{args.user}"
        else:
            args.message = "获取指定用户插件列表需要超级用户权限！"
    elif args.group:
        if args.is_superuser:
            args.group_id = args.group
            args.message += f"群{args.group}"
        else:
            args.message = "获取指定群插件列表需要超级用户权限！"
    elif args.default:
        if args.is_superuser:
            args.type = "default"
            args.message += "默认"
        else:
            args.message = "获取指定群插件列表需要超级用户权限！"

    args.message += "插件列表如下：\n"
    plugin_list = get_plugin_list(args.type, args.user_id, args.group_id)
    args.message += "\n".join(
        f"[{'o' if plugin_list[plugin] else 'x'}] {plugin}" for plugin in plugin_list
    )

    return args


def handle_block(args: Namespace) -> Namespace:

    if args.group and not args.is_admin and not args.is_superuser:
        args.message = "管理群插件需要群管理员权限！"

    if args.globally:
        if args.is_superuser:
            args.type = "global"
            args.message += "全局"
        else:
            args.message = "管理全局插件需要超级用户权限！"
    elif args.user:
        if args.is_superuser:
            args.user_id = args.user
            args.message += f"用户{args.user}"
        else:
            args.message = "管理指定用户插件需要超级用户权限！"
    elif args.group:
        if args.is_superuser:
            args.group_id = args.group
            args.message += f"群{args.group}"
        else:
            args.message = "管理指定群插件需要超级用户权限！"
    elif args.default:
        if args.is_superuser:
            args.type = "default"
            args.message += "默认"
        else:
            args.message = "管理默认插件需要超级用户权限！"

    if args.all:
        args.plugins = [
            plugin for plugin in get_plugin_list(args.type, args.user_id, args.group_id)
        ]

    if args.reverse:
        args.plugins = list(
            filter(
                lambda plugin: plugin not in args.plugins,
                get_plugin_list(args.type, args.user_id, args.group_id),
            )
        )

    args.message += "结果如下："
    result = block_plugin(args.plugins, args.type, args.user_id, args.group_id)
    if result:
        for plugin in result:
            args.message += "\n"
            if result[plugin] is None:
                args.message += f"插件 {plugin} 不存在！"
            elif result[plugin]:
                args.message += f"插件 {plugin} 禁用成功！"
            else:
                args.message += f"插件 {plugin} 已全局启用，请联系超级用户！"
    else:
        args.message = ""

    return args


def handle_unblock(args: Namespace) -> Namespace:

    if args.group and not args.is_admin and not args.is_superuser:
        args.message = "管理群插件需要群管理员权限！"

    if args.globally:
        if args.is_superuser:
            args.type = "global"
            args.message += "全局"
        else:
            args.message = "管理全局插件需要超级用户权限！"
    elif args.user:
        if args.is_superuser:
            args.user_id = args.user
            args.message += f"用户{args.user}"
        else:
            args.message = "管理指定用户插件需要超级用户权限！"
    elif args.group:
        if args.is_superuser:
            args.group_id = args.group
            args.message += f"群{args.group}"
        else:
            args.message = "管理指定群插件需要超级用户权限！"
    elif args.default:
        if args.is_superuser:
            args.type = "default"
            args.message += "默认"
        else:
            args.message = "管理默认插件需要超级用户权限！"

    if args.all:
        args.plugins = [
            plugin for plugin in get_plugin_list(args.type, args.user_id, args.group_id)
        ]

    if args.reverse:
        args.plugins = list(
            filter(
                lambda plugin: plugin not in args.plugins,
                get_plugin_list(args.type, args.user_id, args.group_id),
            )
        )

    args.message += "结果如下："
    result = unblock_plugin(args.plugins, args.type, args.user_id, args.group_id)
    if result:
        for plugin in result:
            args.message += "\n"
            if result[plugin] is None:
                args.message += f"插件 {plugin} 不存在！"
            elif result[plugin]:
                args.message += f"插件 {plugin} 启用成功！"
            else:
                args.message += f"插件 {plugin} 已全局禁用，请联系超级用户！"
    else:
        args.message = ""

    return args


def handle_info(args: Namespace) -> Namespace:

    if not args.is_admin and not args.is_superuser:
        args.message = "获取插件信息需要超级用户权限！"

    args.message = get_plugin_info(args.plugin)


def handle_install(args: Namespace) -> Namespace:
    pass


def handle_uninstall(args: Namespace) -> Namespace:
    pass
