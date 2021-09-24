from nonebot.typing import T_State
from nonebot.matcher import Matcher
from nonebot.message import run_preprocessor
from nonebot.exception import IgnoredException
from nonebot.plugin import on_shell_command, get_loaded_plugins
from nonebot.adapters.cqhttp import (
    Bot,
    Event,
    MessageEvent,
    PrivateMessageEvent,
    GroupMessageEvent,
)

from .parser import npm_parser, PluginManager

npm = on_shell_command("npm", parser=npm_parser, priority=1)

# 在 Matcher 运行前检测其是否启用
@run_preprocessor
async def _(matcher: Matcher, bot: Bot, event: Event, state: T_State):

    plugin_manager = PluginManager()
    plugin = matcher.plugin_name

    conv = {
        "user": [event.user_id] if hasattr(event, "user_id") else [],
        "group": [event.group_id] if hasattr(event, "group_id") else [],
    }

    plugin_manager.update_plugin(
        {
            str(p.name): p.name != "nonebot_plugin_manager" and p.matcher
            for p in get_loaded_plugins()
        }
    )

    if not plugin_manager.get_plugin(conv=conv, perm=1)[plugin]:
        raise IgnoredException(f"Nonebot Plugin Manager has blocked {plugin} !")


@npm.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    args = state["args"]
    args.conv = {
        "user": [event.user_id] if isinstance(event, PrivateMessageEvent) else [],
        "group": [event.group_id] if isinstance(event, GroupMessageEvent) else [],
    }
    args.is_admin = (
        event.sender.role in ["admin", "owner"]
        if isinstance(event, GroupMessageEvent)
        else False
    )
    args.is_superuser = str(event.user_id) in bot.config.superusers

    if hasattr(args, "handle"):
        message = args.handle(args)
        if message:
            await bot.send(event, message)
