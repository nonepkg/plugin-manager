from nonebot.plugin import Matcher, on_shell_command, get_loaded_plugins, export
from nonebot.typing import T_State
from nonebot.exception import IgnoredException
from nonebot.message import run_preprocessor
from nonebot.adapters.cqhttp import Event, Bot, GroupMessageEvent

from . import data
from .parser import parser

# 导出给其他插件使用
export = export()
export.load_ = data.load
export.dump_ = data.dump

# 注册 shell_like 事件响应器
plugin_manager = on_shell_command(
    "npm", aliases=set("plugin"), parser=parser, priority=1
)

# 在 Matcher 运行前检测其是否启用
@run_preprocessor
async def _(matcher: Matcher, bot: Bot, event: Event, state: T_State):
    plugin = matcher.module
    group_id = _get_group_id(event)
    loaded_plugin_list = _get_loaded_plugin_list()
    plugin_list = data.update(data.load(), loaded_plugin_list)

    # 无视本插件的 Mathcer
    if plugin == "nonebot_plugin_manager":
        return

    if group_id in plugin_list[plugin]:
        if not plugin_list[plugin][group_id]:
            raise IgnoredException(f"Nonebot Plugin Manager has blocked {plugin} !")
    else:
        if not plugin_list[plugin]["0"]:
            raise IgnoredException(f"Nonebot Plugin Manager has blocked {plugin} !")


@plugin_manager.handle()
async def _(bot: Bot, event: Event, state: T_State):
    args = state["args"]
    plugin_list = data.load()
    group_id = _get_group_id(event)
    is_admin = _is_admin(event)
    is_superuser = _is_superuser(bot, event)

    if hasattr(args, "handle"):
        await plugin_manager.finish(
            args.handle(args, plugin_list, group_id, is_admin, is_superuser)
        )
    else:
        await plugin_manager.finish(parser.format_help())


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
    if isinstance(event, GroupMessageEvent):
        return event.sender.role in ["admin", "owner"]
    else:
        return False


def _is_superuser(bot: Bot, event: Event) -> bool:
    return str(event.user_id) in bot.config.superusers
