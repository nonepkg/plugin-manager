from argparse import Namespace

from nonebot import get_driver
from nonebot.matcher import Matcher
from nonebot.adapters import Bot, Event
from nonebot.message import run_preprocessor
from nonebot.exception import IgnoredException
from arclet.alconna import Args, Option, Alconna, Subcommand
from nonebot.internal.matcher import matchers as internal_matchers
from nonebot.plugin import (
    PluginMetadata,
    require,
    get_loaded_plugins,
    inherit_supported_adapters,
)

from .handle import Handle
from .manager import plugin_manager

require("nonebot_plugin_alconna")
require("nonebot_plugin_session")
from nonebot_plugin_session import EventSession
from nonebot_plugin_alconna import Match, MultiVar, on_alconna

__plugin_meta__ = PluginMetadata(
    name="新・插件管理器",
    description="基于 import hook 的插件管理",
    usage="""看 README""",
    type="application",
    homepage="https://github.com/nonepkg/plugin-manager",
    supported_adapters=inherit_supported_adapters(
        "nonebot_plugin_alconna", "nonebot_plugin_session"
    ),
)

block_args = (
    Args["plugins", MultiVar(str, "*")],
    Option("-a|--all", default=False),
    Option("-r|--reverse", default=False),
    Option("-u|--user", Args["users", MultiVar(str, "*")]),
    Option("-g|--group", Args["groups", MultiVar(str, "*")]),
)
block = Subcommand("block|disable", *block_args, dest="block")
unblock = Subcommand("unblock|enable", *block_args, dest="unblock")
pnpm = on_alconna(
    Alconna(
        "pnpm",
        block,
        unblock,
    ),
    use_cmd_start=True,
    priority=1,
    block=True,
    aliases={"npm"},
)


@pnpm.assign("block")
async def _(
    session: EventSession,
    plugins: Match[tuple[str]],
    all: Match[bool],
    reverse: Match[bool],
    users: Match[tuple[str]],
    groups: Match[tuple[str]],
    event: Event,
):
    args = Namespace()
    args.is_superuser = True
    args.is_admin = False
    args.plugin = plugins.result
    args.conv = {"user": [session.id1], "group": [session.id2]}
    args.user = [] if not users.available else users.result
    args.group = [] if not groups.available else groups.result
    args.all = all.result if all.available else False
    args.reverse = reverse.result if reverse.available else False
    await pnpm.finish(getattr(Handle, "block")(args))


# 在 Matcher 运行前检测其是否启用
@run_preprocessor
async def _(matcher: Matcher, bot: Bot, event: Event, session: EventSession):
    plugin = matcher.plugin_id

    conv = {
        "user": [session.id1] if session.id1 else [],  # type: ignore
        "group": [session.id2] if session.id2 else [],  # type: ignore
    }

    plugin_manager.update_plugin(
        {
            str(p.id_): p.id_ != __name__ and bool(p.matcher)
            for p in get_loaded_plugins()
        }
    )

    if plugin and not plugin_manager.get_plugin(conv=conv, perm=1)[plugin]:
        await bot.send(event, f"无 {plugin} 的使用权限！")
        raise IgnoredException(f"Nonebot Plugin Manager has blocked {plugin} !")


@get_driver().on_startup
async def _():
    # 不許其他插件待在一级优先级
    for priority in reversed(
        range(1, max(priority for priority in internal_matchers) + 1)
    ):
        internal_matchers[priority + 1] = internal_matchers[priority]
    internal_matchers[1] = [m for m in internal_matchers[1] if m.plugin_id == __name__]
