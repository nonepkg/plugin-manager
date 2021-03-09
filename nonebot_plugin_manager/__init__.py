import os

from nonebot.plugin import get_loaded_plugins, Matcher
from nonebot import on_command
from nonebot.adapters.cqhttp.permission import GROUP_ADMIN, GROUP_OWNER
from nonebot.permission import SUPERUSER
from nonebot.message import run_preprocessor
from nonebot.adapters.cqhttp import Event, Bot
from nonebot.typing import T_State
from nonebot.exception import IgnoredException

DATA_PATH = "data/manager/block_list"

plugin_list = on_command("plugin", permission=SUPERUSER)


@plugin_list.handle()
async def _(bot: Bot, event: Event):
    block_list = get_block_list()
    plugin_list = get_plugin_list()
    message = str(event.get_message()).strip()
    if message == "list":
        result = "插件列表："
        for plugin in plugin_list:
            result += "\n"
            if plugin in block_list:
                result += "× "
            else:
                result += "√ "
            result += plugin
        await bot.send(event, result)
    elif message[:5] == "block":
        plugin = message[6:].strip()
        if plugin in plugin_list and plugin != "nonebot_plugin_manager":
            if plugin in block_list:
                await bot.send(event, "该插件已屏蔽！")
            else:
                block_list.append(plugin)
                set_block_list(block_list)
        else:
            await bot.send(event, "该插件不存在！")
    elif message[:7] == "unblock":
        plugin = message[8:].strip()
        if plugin in plugin_list:
            if not plugin in block_list:
                await bot.send(event, "该插件未被屏蔽！")
            else:
                block_list.remove(plugin)
                set_block_list(block_list)
        else:
            await bot.send(event, "该插件不存在！")


@run_preprocessor
async def _(matcher: Matcher, bot: Bot, event: Event, state: T_State):
    block_list = get_block_list()
    if matcher.module in block_list:
        raise IgnoredException("reason")


def get_block_list() -> list:
    if not os.path.exists(DATA_PATH):
        f = open(DATA_PATH, "w")
        f.close()
    block_list = []
    f = open(DATA_PATH, "r")
    plugin_list = f.read()
    f.close()
    plugin_list = plugin_list.split("\n")
    for plugin in plugin_list:
        if plugin != "":
            block_list.append(plugin)
    return block_list


def get_plugin_list() -> list:
    plugin_list = []
    for plugin in get_loaded_plugins():
        plugin_list.append(plugin.name)
    return plugin_list


def set_block_list(block_list):
    f = open(DATA_PATH, "w")
    f.writelines(plugin + "\n" for plugin in block_list)
    f.close()
