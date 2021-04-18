from nonebot.plugin import Matcher, on_shell_command, get_loaded_plugins, export
from nonebot.typing import T_State
from nonebot.exception import IgnoredException
from nonebot.message import run_preprocessor
from nonebot.adapters.cqhttp import Event, Bot, PrivateMessageEvent, GroupMessageEvent

from .parser import (
    npm_parser,
    block_plugin,
    unblock_plugin,
    get_plugin_list,
    auto_update_plugin_list,
)

# 导出给其他插件使用
export = export()
export.block_plugin = block_plugin
export.unblock_plugin = unblock_plugin
export.get_plugin_list = get_plugin_list

# 注册 shell_like 事件响应器
plugin_manager = on_shell_command("npm", parser=npm_parser, priority=1)

# 在 Matcher 运行前检测其是否启用
@run_preprocessor
async def _(matcher: Matcher, bot: Bot, event: Event, state: T_State):

    plugin = matcher.module.split(".", maxsplit=1)[0]
    user_id = event.user_id if isinstance(event, PrivateMessageEvent) else None
    group_id = event.group_id if isinstance(event, GroupMessageEvent) else None

    auto_update_plugin_list(
        [
            str(plugin.name)
            for plugin in filter(
                lambda plugin: plugin.name != "nonebot_plugin_manager"
                and plugin.matcher,
                get_loaded_plugins(),
            )
        ]
    )

    # 无视本插件的 Mathcer
    if plugin == "nonebot_plugin_manager":
        return

    if not get_plugin_list(user_id=user_id, group_id=group_id)[plugin]:
        raise IgnoredException(f"Nonebot Plugin Manager has blocked {plugin} !")


@plugin_manager.handle()
async def _(bot: Bot, event: Event, state: T_State):
    args = state["args"]
    args.type = None
    args.message = ""
    args.user_id = event.user_id if isinstance(event, PrivateMessageEvent) else None
    args.group_id = event.group_id if isinstance(event, GroupMessageEvent) else None
    args.is_admin = (
        event.sender.role in ["admin", "owner"]
        if isinstance(event, GroupMessageEvent)
        else False
    )
    args.is_superuser = str(event.user_id) in bot.config.superusers

    if hasattr(args, "handle"):
        args = args.handle(args)
        if args.message:
            await bot.send(event, args.message)
