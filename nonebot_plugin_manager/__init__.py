from nonebot.matcher import Matcher
from nonebot.adapters import Bot, Event
from nonebot.message import run_preprocessor
from nonebot.exception import IgnoredException
from nonebot import get_driver, get_loaded_plugins
from nonebot.internal.matcher import matchers as internal_matchers
from nonebot.plugin import PluginMetadata, require, inherit_supported_adapters
from arclet.alconna import Args, Option, Alconna, MultiVar, Subcommand

require("nonebot_plugin_localstore")
require("nonebot_plugin_alconna")
require("nonebot_plugin_session")

from nonebot_plugin_alconna import Match, Query, on_alconna

from .manager import plugin_manager
from .params import UserId, RealmId

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
    Option("-r|--reverse", default=False),
    Option("-u|--user", Args["users", MultiVar(str, "*")]),
    Option("-g|--group", Args["groups", MultiVar(str, "*")]),
)
enable = Subcommand("enable|unblock", *_able_args, dest="enable")
disable = Subcommand("disable|block", *_able_args, dest="disable")
pnpm = on_alconna(
    Alconna("pnpm", enable, disable),
    use_cmd_start=True,
    priority=1,
    block=True,
    aliases={"npm"},
)


@pnpm.assign("enable")
@pnpm.assign("disable")
async def _(
    plugins: Match[tuple[str]],
    all: Match[bool],
    reverse: Match[bool],
    users: Match[tuple[str]],
    groups: Match[tuple[str]],
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
    # TODO: refactor
    for plugin in plugins.result:
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
                message += f"- - {e}\n"
        for user in users.result if users.available else []:
            plugin_manager._able_plugin(
                plugin,
                user_id,
                enabled.result,
                user,
                scope=realm_id,
            )
        for group in groups.result if groups.available else []:
            plugin_manager._able_plugin(
                plugin,
                user_id,
                enabled.result,
                realm_id=group,
                scope=realm_id,
            )
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
    if plugin is None or plugin == __name__:
        return

    if not plugin_manager.check_perm(plugin, user_id, realm_id, str(bot.self_id)):
        await bot.send(event, f"无 {plugin} 的使用权限！")
        raise IgnoredException(f"Nonebot Plugin Manager has blocked {plugin} !")


@get_driver().on_startup
async def _():
    await plugin_manager._monitor.load()
    for plugin in get_loaded_plugins():
        plugin_manager.init_plugin(plugin.id_)

    # 不許其他插件待在一级优先级
    for priority in reversed(
        range(1, max(priority for priority in internal_matchers) + 1)
    ):
        internal_matchers[priority + 1] = internal_matchers[priority]
    internal_matchers[1] = [m for m in internal_matchers[1] if m.plugin_id == __name__]
