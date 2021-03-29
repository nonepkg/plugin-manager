from nonebot.plugin import Matcher, on_shell_command, get_loaded_plugins, export
from nonebot.typing import T_State
from nonebot.exception import IgnoredException
from nonebot.message import run_preprocessor
from nonebot.adapters.cqhttp import Event, Bot, GroupMessageEvent

from .data import (
    block_plugin,
    unblock_plugin,
    get_group_plugin_list,
    auto_update_plugin_list,
)
from .parser import npm_parser

# 导出给其他插件使用
export = export()
export.block_plugin = block_plugin
export.unblock_plugin = unblock_plugin
export.get_group_plugin_list = get_group_plugin_list

# 注册 shell_like 事件响应器
plugin_manager = on_shell_command("npm", parser=npm_parser, priority=1)

# 在 Matcher 运行前检测其是否启用
@run_preprocessor
async def _(matcher: Matcher, bot: Bot, event: Event, state: T_State):
    plugin = matcher.module
    group_id = _get_group_id(event)

    auto_update_plugin_list(_get_loaded_plugin_list())

    # 无视本插件的 Mathcer
    if plugin == "nonebot_plugin_manager":
        return

    if get_group_plugin_list(group_id)[plugin]:
        raise IgnoredException(f"Nonebot Plugin Manager has blocked {plugin} !")


@plugin_manager.handle()
async def _(bot: Bot, event: Event, state: T_State):
    args = state["args"]
    group_id = _get_group_id(event)
    is_admin = _is_admin(event)
    is_superuser = _is_superuser(bot, event)

    if hasattr(args, "handle"):
        await plugin_manager.finish(args.handle(args, group_id, is_admin, is_superuser))


# 获取插件列表，并自动排除本插件
def _get_loaded_plugin_list() -> list:
    return list(
        filter(
            lambda plugin: plugin != "nonebot_plugin_manager",
            map(lambda plugin: plugin.name, get_loaded_plugins()),
        )
    )


def _get_group_id(event: Event) -> str:
    return str(event.group_id if isinstance(event, GroupMessageEvent) else 0)


def _is_admin(event: Event) -> bool:
    return (
        event.sender.role in ["admin", "owner"]
        if isinstance(event, GroupMessageEvent)
        else False
    )


def _is_superuser(bot: Bot, event: Event) -> bool:
    return str(event.user_id) in bot.config.superusers
