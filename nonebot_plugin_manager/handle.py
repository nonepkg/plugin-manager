from argparse import Namespace

from .plugin import *


def handle_list(args: Namespace) -> str:

    message = ""

    if args.user:
        if args.is_superuser:
            args.mode = "user"
            args.user_id = args.user
            message = f"用户 {args.user}"
        else:
            return "获取指定用户插件列表需要超级用户权限！"
    elif args.group:
        if args.is_superuser:
            args.mode = "group"
            args.group_id = args.group
            message = f"群 {args.group}"
        else:
            return "获取指定群插件列表需要超级用户权限！"
    else:
        args.mode = ""

    if args.ignore:
        args.mode += "+"

    if args.store:
        if args.is_superuser:
            message = "商店"
            plugin_list = get_store_pulgin_list()
        else:
            return "获取商店插件列表需要超级用户权限！"
    else:
        message += "插件列表如下：\n"
        plugin_list = PluginList().get_plugins(args.mode, args.user_id, args.group_id)
        message += "\n".join(
            f"[{'o' if plugin_list[plugin] else 'x'}] {plugin}"
            for plugin in plugin_list
        )
        return message


def handle_set(args: Namespace) -> str:
    message = ""
    plugin_list = PluginList()
    args.user_id = [args.user_id] if args.user_id else []
    args.group_id = [args.group_id] if args.group_id else []
    if not args.is_superuser:
        return "设置插件模式需要超级用户权限！"

    plugins = plugin_list.get_plugins()

    if args.all:
        args.plugins = list(filter(lambda plugin: plugins[plugin], plugins))
    if args.reverse:
        args.plugins = list(filter(lambda plugin: plugin not in args.plugins, plugins))

    result = plugin_list.set_plugin(args.plugins, args.mode)
    message += (
        "用户: " if args.user_id else "" + ",".join([str(id) for id in args.user_id])
    )
    message += (
        "群: " if args.group_id else "" + ",".join([str(id) for id in args.group_id])
    )
    message += "的插件列表操作结果如下："
    for plugin in result:
        message += "\n"
        if result[plugin]:
            message += f"插件 {plugin} 的模式成功设置为 {args.mod}！"
        else:
            message += f"插件 {plugin} 不存在或已关闭编辑权限！"
    return message


def handle_block(args: Namespace) -> str:

    message = ""
    plugin_list = PluginList()
    args.user_id = [args.user_id] if args.user_id else []
    args.group_id = [args.group_id] if args.group_id else []
    if args.group_id:
        if not args.is_admin:
            return "管理群插件需要群管理员权限！"
    else:
        if not args.is_superuser:
            return "管理用户插件需要超级用户权限！"

    if args.user or args.group:
        args.user_id = args.user
        args.group_id = args.group

    plugins = plugin_list.get_plugins()

    if args.all:
        args.plugins = list(filter(lambda plugin: plugins[plugin], plugins))
    if args.reverse:
        args.plugins = list(filter(lambda plugin: plugin not in args.plugins, plugins))

    result = plugin_list.block_plugin(
        args.plugins, args.user_id, args.group_id, args.is_superuser
    )
    message += (
        "用户: " if args.user_id else "" + ",".join([str(id) for id in args.user_id])
    )
    message += (
        "群: " if args.group_id else "" + ",".join([str(id) for id in args.group_id])
    )
    message += "的插件列表操作结果如下："
    for plugin in result:
        message += "\n"
        if result[plugin]:
            message += f"插件 {plugin} 禁用成功！"
        else:
            message += f"插件 {plugin} 不存在或已关闭编辑权限！"
    return message


def handle_unblock(args: Namespace) -> str:

    message = ""
    plugin_list = PluginList()
    args.user_id = [args.user_id] if args.user_id else []
    args.group_id = [args.group_id] if args.group_id else []
    if args.group_id:
        if not args.is_admin:
            return "管理群插件需要群管理员权限！"
    else:
        if not args.is_superuser:
            return "管理用户插件需要超级用户权限！"

    if args.user or args.group:
        args.user_id = args.user
        args.group_id = args.group

    plugins = plugin_list.get_plugins()

    if args.all:
        args.plugins = list(filter(lambda plugin: plugins[plugin], plugins))
    if args.reverse:
        args.plugins = list(filter(lambda plugin: plugin not in args.plugins, plugins))

    result = plugin_list.unblock_plugin(
        args.plugins, args.user_id, args.group_id, args.is_superuser
    )
    message += (
        "用户: " if args.user_id else "" + ",".join([str(id) for id in args.user_id])
    )
    message += (
        "群: " if args.group_id else "" + ",".join([str(id) for id in args.group_id])
    )
    message += "的插件列表操作结果如下："
    for plugin in result:
        message += "\n"
        if result[plugin]:
            message += f"插件 {plugin} 启用成功！"
        else:
            message += f"插件 {plugin} 不存在或已关闭编辑权限！"
    return message


def handle_info(args: Namespace) -> str:

    if not args.is_admin and not args.is_superuser:
        return "获取插件信息需要超级用户权限！"

    return get_plugin_info(args.plugin)


def handle_install(args: Namespace) -> str:
    pass


def handle_uninstall(args: Namespace) -> str:
    pass
