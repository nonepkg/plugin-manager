import os
import json

from nonebot.plugin import Matcher, get_loaded_plugins, on_shell_command
from nonebot.rule import ArgumentParser
from nonebot.typing import T_State
from nonebot.exception import IgnoredException
from nonebot.message import run_preprocessor
from nonebot.adapters.cqhttp import Event, Bot, GroupMessageEvent

DATA_PATH = "data/manager/setting.json"

# 在 Matcher 运行前检测其是否启用
@run_preprocessor
async def _(matcher: Matcher, bot: Bot, event: Event, state: T_State):
    if matcher.module == "nonebot_plugin_manager":
        return
    group_id = event.group_id if isinstance(event, GroupMessageEvent) else 0
    setting = load_setting(group_id)
    if not matcher.module in setting:
        setting[matcher.module] = True
        update_setting(group_id, setting)
    if not setting[matcher.module]:
        raise IgnoredException("Nonebot Plugin Manager has blocked this plugin !")


parser = ArgumentParser("npm")
subparsers = parser.add_subparsers()

block_parser = subparsers.add_parser("block", help="block plugin")
block_parser.add_argument("plugins", nargs="*")
block_parser.add_argument("-d", "--default", action="store_true")
block_parser.add_argument("-a", "--all", action="store_true")
block_parser.add_argument("-g", "--group")
block_parser.set_defaults(command="block")

unblock_parser = subparsers.add_parser("unblock", help="unblock plugin")
unblock_parser.add_argument("plugins", nargs="*")
unblock_parser.add_argument("-d", "--default", action="store_true")
block_parser.add_argument("-g", "--group")
unblock_parser.set_defaults(command="unblock")

list_parser = subparsers.add_parser("list", help="show plugin list")
list_parser.add_argument("-d", "--default", action="store_true")
list_parser.add_argument("-g", "--group")
list_parser.set_defaults(command="list")

plugin_manager = on_shell_command("npm", parser=parser)


@plugin_manager.handle()
async def _(bot: Bot, event: Event, state: T_State):
    group_id = event.group_id if isinstance(event, GroupMessageEvent) else 0
    plugin_list = get_plugin_list()
    message = ""

    if state["args"].default:
        group_id = 0
        message += "全局"

    if state["args"].command == "list":
        setting = load_setting(group_id)
        message += "插件列表如下："
        for plugin in plugin_list:
            message += f'\n[{"o" if setting[plugin] else "x"}] {plugin}'
        await plugin_manager.finish(message)

    if state["args"].command == "block":
        setting = load_setting(group_id)
        message += "结果如下："
        for plugin in state["args"].plugins if not state["args"].all else plugin_list:
            message += "\n"
            if plugin in plugin_list:
                if setting[plugin]:
                    setting[plugin] = False
                    message += f"插件 {plugin} 屏蔽成功！"
                else:
                    message += f"插件 {plugin} 已经屏蔽！"
            else:
                message += f"插件 {plugin} 不存在！"
        update_setting(group_id, setting)
        await plugin_manager.finish(message)

    if state["args"].command == "unblock":
        setting = load_setting(group_id)
        message = "结果如下："
        for plugin in state["args"].plugins if not state["args"].all else plugin_list:
            message += "\n"
            if plugin in plugin_list:
                if not setting[plugin]:
                    setting[plugin] = True
                    message += f"插件 {plugin} 启用成功！"
                else:
                    message += f"插件 {plugin} 已经启用！"
            else:
                message += f"插件 {plugin} 不存在！"
        update_setting(group_id, setting)
        await plugin_manager.finish(message)


# 获取插件列表，并自动排除 npm
def get_plugin_list() -> list:
    plugin_list = []
    for plugin in get_loaded_plugins():
        plugin_list.append(plugin.name)
    plugin_list.remove("nonebot_plugin_manager")
    return plugin_list


# 当 setting.json 不存在时自动创建 setting.json
def create_setting():
    if not os.path.exists(DATA_PATH):
        os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
        setting = {}
        with open(DATA_PATH, "w", encoding="utf-8") as f:
            for plugin in get_plugin_list():
                setting["0"] = {}
                setting["0"][plugin] = True
            json.dump(setting, f, indent=4, separators=(",", ": "))


# 获取指定群的设置，如果获取不到则采用全局设置
def load_setting(group_id: int) -> dict:
    create_setting()
    full_setting = json.load(open(DATA_PATH, "r", encoding="utf-8"))
    if str(group_id) not in full_setting.keys():
        return full_setting["0"]
    return full_setting[str(group_id)]


def update_setting(group_id: int, setting: dict):
    full_setting = json.load(open(DATA_PATH, "r", encoding="utf-8"))
    full_setting[str(group_id)] = setting
    json.dump(
        full_setting,
        open(DATA_PATH, "w", encoding="utf-8"),
        indent=4,
        separators=(",", ": "),
    )
