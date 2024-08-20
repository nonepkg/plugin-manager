from typing import Union

from nonebot.matcher import Matcher
from nonebot.adapters import Bot, Event
from nonebot.message import run_preprocessor
from nonebot.exception import IgnoredException
from nonebot import get_driver, get_loaded_plugins
from nonebot.internal.matcher import matchers as internal_matchers
from arclet.alconna import Args, Option, Alconna, MultiVar, Subcommand
from nonebot.plugin import PluginMetadata, require, inherit_supported_adapters

require("nonebot_plugin_localstore")
require("nonebot_plugin_alconna")
require("nonebot_plugin_session")

from nonebot_plugin_alconna import At, Match, Query, on_alconna

from .manager import plugin_manager
from .params import UserId, RealmId, Platform

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

_able_args = (
    Args["plugins", MultiVar(str, "*")],
    Option("-a|--all", default=False),
    Option("-u|--user", Args["users", MultiVar(str, "*")]),
    Option("-g|--group", Args["groups", MultiVar(str, "*")]),
)
enable = Subcommand("enable|unblock", *_able_args, dest="enable")
disable = Subcommand("disable|block", *_able_args, dest="disable")
_ban_args = (
    Args["users", MultiVar(Union[At, str])],
    Option("-p|--plugin", Args["plugins", MultiVar(str, "*")]),
    Option("-g|--group", Args["groups", MultiVar(str, "*")]),
)
ban = Subcommand("ban", *_ban_args, dest="ban")
unban = Subcommand("unban", *_ban_args, dest="unban")
_op_args = (
    Args["users", MultiVar(Union[At, str])],
    Option("-g|--group", Args["groups", MultiVar(str, "*")]),
)
op = Subcommand("op", *_able_args, dest="op")
deop = Subcommand("deop", *_able_args, dest="deop")
pnpm = on_alconna(
    Alconna("pnpm", enable, disable, ban, unban, op, deop),
    use_cmd_start=True,
    priority=1,
    block=True,
    aliases={"npm"},
)


# TODO: refactor
@pnpm.assign("ban")
@pnpm.assign("unban")
async def _(
    users: Match[tuple[Union[At, str]]],
    plugins: Match[tuple[str]],
    groups: Match[tuple[str]],  # 還没写
    bot: Bot,
    platform: Platform,
    user_id: UserId,
    realm_id: RealmId,
    enabled: Query[bool] = Query("subcommands.unban.value", False),
):
    user_id = (
        "root"
        if user_id in bot.config.superusers
        or user_id.split(":", 1)[1] in bot.config.superusers
        else user_id
    )
    message = f"在当前上下文中{'解禁' if enabled.result else '禁用'}用户的结果：\n"
    for plugin in plugins.result if plugins.available else ["/"]:
        message += f"- 插件 {plugin}：\n"
        for user in users.result if users.available else []:
            if isinstance(user, At):
                user = f"{platform}:{user.target}"
            elif ":" not in user:
                user = f"{platform}:{user}"
            try:
                plugin_manager._able_plugin(
                    plugin,
                    user_id,
                    enabled.result,
                    user,
                    scope=realm_id,
                )
                message += f"- - {user} 成功\n"
            except Exception as e:
                message += f"- - {user} {e}\n"
    await plugin_manager._monitor.save()
    await pnpm.finish(message)


# TODO: refactor
@pnpm.assign("enable")
@pnpm.assign("disable")
async def _(
    plugins: Match[tuple[str]],
    all: Match[bool],
    users: Match[tuple[str]],  # 還沒寫
    groups: Match[tuple[str]],  # 还没写
    bot: Bot,
    user_id: UserId,
    realm_id: RealmId,
    enabled: Query[bool] = Query("subcommands.enable.value", False),
):
    user_id = (
        "root"
        if user_id in bot.config.superusers
        or user_id.split(":", 1)[1] in bot.config.superusers
        else user_id
    )
    message = f"在当前上下文中{'启用' if enabled.result else '禁用'}插件的结果：\n"
    for plugin in plugins.result if not all.available else ["/"]:
        message += f"- 插件 {plugin}：\n"
        if not (users.available or groups.available):
            try:
                plugin_manager._able_plugin(
                    plugin,
                    user_id,
                    enabled.result,
                    user_id=user_id,
                    realm_id=realm_id,
                    scope=realm_id,
                )
                message += f"- - {realm_id or user_id} 成功\n"
            except Exception as e:
                message += f"- - {realm_id or user_id} {e}\n"
    await plugin_manager._monitor.save()
    await pnpm.finish(message)


@pnpm.assign("op")
@pnpm.assign("deop")
async def _(
    groups: Match[tuple[str]],  # 还没写
    users: Match[tuple[Union[At, str]]],
    bot: Bot,
    platform: Platform,
    user_id: UserId,
    realm_id: RealmId,
    enabled: Query[bool] = Query("subcommands.op.value", False),
):
    if (
        user_id not in bot.config.superusers
        or user_id.split(":", 1)[1] not in bot.config.superusers
    ):
        await pnpm.finish("无超管权限")
    message = f"在当前上下文中{'设置' if enabled.result else '移除'}管理员的结果：\n"
    for user in users.result if users.available else []:
        if isinstance(user, At):
            user = f"{platform}:{user.target}"
        elif ":" not in user:
            user = f"{platform}:{user}"
        try:
            plugin_manager._op_user(user, realm_id, enabled.result)
            message += f"- - {user} 成功\n"
        except Exception as e:
            message += f"- - {user} {e}\n"
    await plugin_manager._monitor.save()
    await pnpm.finish(message)


@run_preprocessor
async def _(
    bot: Bot,
    event: Event,
    matcher: Matcher,
    user_id: UserId,
    realm_id: RealmId,
):
    plugin = matcher.plugin_id
    plugin_manager.get_user(user_id, str(bot.self_id), realm_id)

    if plugin is None or plugin == __name__:
        return
    if not plugin_manager.check_perm(plugin, user_id, realm_id, str(bot.self_id)):
        await bot.send(event, f"无 {plugin} 的使用权限！")
        raise IgnoredException(f"Nonebot Plugin Manager has blocked {plugin} !")


@get_driver().on_startup
async def _():
    await plugin_manager._monitor.load()
    for plugin in get_loaded_plugins():
        if plugin.id_ == __name__:
            continue
        plugin_manager.init_plugin(plugin.id_)

    # 不許其他插件待在一级优先级
    for priority in reversed(
        range(1, max(priority for priority in internal_matchers) + 1)
    ):
        internal_matchers[priority + 1] = internal_matchers[priority]
    internal_matchers[1] = [m for m in internal_matchers[1] if m.plugin_id == __name__]
