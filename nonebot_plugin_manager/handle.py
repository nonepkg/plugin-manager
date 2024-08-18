from argparse import Namespace

from .manager import plugin_manager


class Handle:
    @classmethod
    async def block(cls, args: Namespace) -> str:
        result = {}
        for p in args.plugin:
            for user in args.users:
                try:
                    plugin_manager._able_plugin(
                        p, args.user_id, False, user_id=user, scope=args.scope
                    )
                except Exception:
                    result[p] = False
                    continue
                result[p] = True
            for group in args.groups:
                try:
                    result[p] = plugin_manager._able_plugin(
                        p, args.user_id, False, realms_id=group, scope=args.scope
                    )
                except:
                    result[p] = False
                    continue
                result[p] = True
        await plugin_manager._monitor.save()
        message = ""
        for plugin, value in result.items():
            message += "\n"
            if value:
                message += f"插件 {plugin} 禁用成功！"
            else:
                message += f"插件 {plugin} 不存在或已关闭编辑权限！"
        return message

    @classmethod
    async def unblock(cls, args: Namespace) -> str:
        result = {}
        for p in args.plugin:
            for user in args.users:
                try:
                    plugin_manager._able_plugin(
                        p, args.user_id, False, user_id=user, scope=args.scope
                    )
                except Exception:
                    result[p] = False
                    continue
                result[p] = True
            for group in args.groups:
                try:
                    result[p] = plugin_manager._able_plugin(
                        p, args.user_id, False, realms_id=group, scope=args.scope
                    )
                except:
                    result[p] = False
                    continue
                result[p] = True
        await plugin_manager._monitor.save()
        message = ""
        for plugin, value in result.items():
            message += "\n"
            if value:
                message += f"插件 {plugin} 启用成功！"
            else:
                message += f"插件 {plugin} 不存在或已关闭编辑权限！"
        return message

    # 以下功能尚未实现

    @classmethod
    def install(cls, args: Namespace) -> str:
        return ""

    @classmethod
    def uninstall(cls, args: Namespace) -> str:
        return ""
