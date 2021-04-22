from nonebot.plugin import Matcher, on_shell_command, get_loaded_plugins, export
from nonebot.typing import T_State
from nonebot.exception import IgnoredException
from nonebot.message import run_preprocessor
from nonebot.adapters.cqhttp import (
    MessageEvent,
    Bot,
    PrivateMessageEvent,
    GroupMessageEvent,
)

from .parser import npm_parser, PluginList

# 导出给其他插件使用
export = export()
export.plugin_list = PluginList()

# 注册 shell_like 事件响应器
plugin_manager = on_shell_command("npm", parser=npm_parser, priority=1)

# 在 Matcher 运行前检测其是否启用
@run_preprocessor
async def _(matcher: Matcher, bot: Bot, event: MessageEvent, state: T_State):

    plugin = matcher.module.split(".", maxsplit=1)[0]
    plugin_list = PluginList()
    user_id = event.user_id
    group_id = event.group_id if isinstance(event, GroupMessageEvent) else None

    plugin_list.update_plugin(
        {
            str(plugin.name): plugin.name != "nonebot_plugin_manager" and plugin.matcher
            for plugin in get_loaded_plugins()
        }
    )
    if not plugin_list.get_plugins("+", user_id, group_id)[plugin]:
        raise IgnoredException(f"Nonebot Plugin Manager has blocked {plugin} !")


@plugin_manager.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    args = state["args"]
    args.user_id = event.user_id if isinstance(event, PrivateMessageEvent) else None
    args.group_id = event.group_id if isinstance(event, GroupMessageEvent) else None
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
