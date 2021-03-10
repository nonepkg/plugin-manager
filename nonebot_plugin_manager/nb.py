from nonebot.plugin import get_loaded_plugins
from nonebot.plugin import Matcher, on_shell_command
from nonebot.typing import T_State
from nonebot.exception import IgnoredException
from nonebot.message import run_preprocessor
from nonebot.adapters.cqhttp import Event, Bot, GroupMessageEvent

from .setting import *
from .command import *
from .parse import *

# 在 Matcher 运行前检测其是否启用
@run_preprocessor
async def _(matcher: Matcher, bot: Bot, event: Event, state: T_State):
    update_default_setting(_get_plugin_list())

    plugin = matcher.module

    # 无视本插件的 Mathcer
    if plugin == "nonebot_plugin_manager":
        return

    group_id = _get_group_id(event)

    setting = load_setting[group_id]
    if plugin not in setting:
        setting = load_setting(0)

    if not setting[plugin]:
        raise IgnoredException(f"Nonebot Plugin Manager has blocked {plugin} !")


plugin_manager = on_shell_command("npm", parser=parser)


@plugin_manager.handle()
async def _(bot: Bot, event: Event, state: T_State):
    args = state["args"]
    group_id = _get_group_id(event)
    is_admin = _is_admin(event)
    is_superuser = _is_superuser(bot, event)
    plugin_list = _get_plugin_list()

    if args.command == "list":
        await plugin_manager.finish(
            command_list(args, plugin_list, group_id, is_admin, is_superuser)
        )
    elif args.command == "block":
        await plugin_manager.finish(
            command_block(args, plugin_list, group_id, is_admin, is_superuser)
        )
    elif args.command == "unblock":
        await plugin_manager.finish(
            command_unblock(args, plugin_list, group_id, is_admin, is_superuser)
        )


# 获取插件列表，并自动排除本插件
def _get_plugin_list() -> list:
    plugin_list = []
    for plugin in get_loaded_plugins():
        plugin_list.append(plugin.name)
    plugin_list.remove("nonebot_plugin_manager")
    return plugin_list


def _get_group_id(event: Event) -> int:
    return event.group_id if isinstance(event, GroupMessageEvent) else 0


def _is_admin(event: Event) -> bool:
    if isinstance(event, GroupMessageEvent):
        return event.sender.role in ["admin", "owner"]
    else:
        return False


def _is_superuser(bot: Bot, event: Event) -> bool:
    return str(event.user_id) in bot.config.superusers
