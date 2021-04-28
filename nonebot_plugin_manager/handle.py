from argparse import Namespace

from .plugin import *


def handle_ls(args: Namespace) -> str:
    if args.store:
        if args.is_superuser:
            message = "插件商店：\n"
            plugin = get_store_pulgin_list()
        else:
            return "获取插件商店需要超级用户权限！"
    else:
        if args.user or args.group:
            if args.is_superuser:
                args.conv = {"user": args.user, "group": args.group}
            else:
                return "获取指定会话的插件列表需要超级用户权限！"

        for t in args.conv:
            for i in args.conv[t]:
                message = f"{'用户' if t == 'user' else '群'}({i}) 的插件列表：\n"

        plugin_manager = PluginManager()

        plugin = plugin_manager.get_plugin(args.conv, 1)
        if not args.all:
            plugin = {
                p: plugin[p]
                for p in plugin
                if plugin_manager.get_plugin(args.conv, 4)[p]
            }

    message = message + "\n".join(f"[{'o' if plugin[p] else 'x'}] {p}" for p in plugin)
    return message


def handle_info(args: Namespace) -> str:
    if not args.is_superuser:
        return "获取插件信息需要超级用户权限！"
    return get_plugin_info(args.plugin)


def handle_chmod(args: Namespace) -> str:
    if not args.is_superuser:
        return "设置插件权限需要超级用户权限！"
    else:
        plugin_manager = PluginManager()
        plugin = plugin_manager.get_plugin(perm=4)

        if args.all:
            args.plugin = list(p for p in plugin)
        if args.reverse:
            args.plugin = list(filter(lambda p: p not in args.plugin, plugin))

        # 这里或者 chomod_plugin 里之后应该有个将 r w x 翻译成 4 2 1 的处理
        result = plugin_manager.chmod_plugin(args.plugin, args.mode)

        message = "\n".join(
            f"插件 {p} 的权限成功设置为 {args.mode}！" if result[p] else f"插件 {p} 不存在！"
            for p in result
        )
    return message


def handle_block(args: Namespace) -> str:

    plugin_manager = PluginManager()
    plugin = plugin_manager.get_plugin(perm=2)

    if args.all:
        args.plugin = list(p for p in plugin)
    if args.reverse:
        args.plugin = list(filter(lambda p: p not in args.plugin, plugin))

    result = {}
    if not args.is_superuser:
        for p in plugin:
            if p in args.plugin and not plugin[p]:
                args.plugin.pop(p)
                result[p] = False

    if args.user or args.group:
        if args.is_superuser:
            args.conv = {"user": args.user, "group": args.group}
        else:
            return "管理指定会话的插件需要超级用户权限！"

    result.update(plugin_manager.block_plugin(args.plugin, args.conv))

    message = ""
    for t in args.conv:
        if args.conv[t]:
            message += "用户" if t == "user" else "群"
            message += ",".join(str(i) for i in args.conv[t])
    message += "中："

    for plugin in result:
        message += "\n"
        if result[plugin]:
            message += f"插件 {plugin} 禁用成功！"
        else:
            message += f"插件 {plugin} 不存在或已关闭编辑权限！"
    return message


def handle_unblock(args: Namespace) -> str:

    plugin_manager = PluginManager()
    plugin = plugin_manager.get_plugin(perm=2)

    if args.all:
        args.plugin = list(p for p in plugin)
    if args.reverse:
        args.plugin = list(filter(lambda p: p not in args.plugin, plugin))

    result = {}
    if not args.is_superuser:
        for p in plugin:
            if p in args.plugin and not plugin[p]:
                args.plugin.pop(p)
                result[p] = False

    if args.user or args.group:
        if args.is_superuser:
            args.conv = {"user": args.user, "group": args.group}
        else:
            return "管理指定会话的插件需要超级用户权限！"

    result.update(plugin_manager.unblock_plugin(args.plugin, args.conv))

    message = ""
    for t in args.conv:
        if args.conv[t]:
            message += "用户" if t == "user" else "群"
            message += ",".join(str(i) for i in args.conv[t])
    message += "中："

    for plugin in result:
        message += "\n"
        if result[plugin]:
            message += f"插件 {plugin} 启用成功！"
        else:
            message += f"插件 {plugin} 不存在或已关闭编辑权限！"
    return message


# 以下功能尚未实现


def handle_install(args: Namespace) -> str:
    pass


def handle_uninstall(args: Namespace) -> str:
    pass
