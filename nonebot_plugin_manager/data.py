import yaml
from pathlib import Path
from typing import Dict, List, Optional, Union


class PluginList:
    __path: Path
    __plugin_list: Dict[str, Dict[str, Union[bool, Dict[int, bool]]]]

    def __init__(self, path: Path = Path() / "data" / "manager" / "plugin_list.yml"):
        self.__path = path
        self.__load()

    def get_plugin(
        self,
        type: Optional[str] = None,
        user_id: Optional[int] = None,
        group_id: Optional[int] = None,
    ) -> Dict[str, bool]:
        result = {}
        for plugin in self.__plugin_list:
            if type == "ignore" or not self.__plugin_list[plugin]["ignore"]:
                if self.__plugin_list[plugin]["global"]:
                    if (
                        not type == "group"
                        and user_id in self.__plugin_list[plugin]["user"]
                    ):
                        if self.__plugin_list[plugin]["user"][user_id]:
                            result[plugin] = True
                        else:
                            result[plugin] = False
                    else:
                        if (
                            not type == "user"
                            and group_id in self.__plugin_list[plugin]["group"]
                        ):
                            if self.__plugin_list[plugin]["group"][group_id]:
                                result[plugin] = True
                            else:
                                result[plugin] = False
                        else:
                            result[plugin] = True
                else:
                    if (
                        not type == "user"
                        and group_id in self.__plugin_list[plugin]["group"]
                    ):
                        if self.__plugin_list[plugin]["group"][group_id]:
                            result[plugin] = True
                        else:
                            result[plugin] = False
                    else:
                        if (
                            not type == "group"
                            and user_id in self.__plugin_list[plugin]["user"]
                        ):
                            if self.__plugin_list[plugin]["user"][user_id]:
                                result[plugin] = True
                            else:
                                result[plugin] = False
                        else:
                            result[plugin] = False
        return result

    def update_plugin(self, plugins: Dict[str, bool]) -> "PluginList":
        other = PluginList().__unignore_plugin(plugins).__ignore_plugin(plugins)
        self.__unignore_plugin(plugins).__ignore_plugin(other.get_plugin()).__dump()
        return self

    # 禁用插件
    def block_plugin(
        self,
        plugins: List[str],
        type: Optional[str] = None,
        user_id: Optional[int] = None,
        group_id: Optional[int] = None,
    ) -> Dict[str, bool]:
        result = {}
        for plugin in plugins:
            if (
                plugin in self.__plugin_list
                and not self.__plugin_list[plugin]["ignore"]
                and self.__plugin_list[plugin]["global"]
            ):
                result[plugin] = True
                if type == "global":
                    self.__plugin_list[plugin] = False
                elif type == "user" or user_id:
                    self.__plugin_list[plugin]["user"][user_id] = False
                elif type == "group" or group_id:
                    self.__plugin_list[plugin]["group"][group_id] = False
            else:
                result[plugin] = False
        self.__dump()
        return result

    # 解禁插件
    def unblock_plugin(
        self,
        plugins: List[str],
        type: Optional[str] = None,
        user_id: Optional[int] = None,
        group_id: Optional[int] = None,
    ) -> Dict[str, bool]:
        result = {}
        for plugin in plugins:
            if (
                plugin in self.__plugin_list
                and not self.__plugin_list[plugin]["ignore"]
                and (type == "global" or self.__plugin_list[plugin]["global"])
            ):
                result[plugin] = True
                if type == "global":
                    self.__plugin_list[plugin] = True
                elif type == "user" or user_id:
                    self.__plugin_list[plugin]["user"][user_id] = True
                elif type == "group" or group_id:
                    self.__plugin_list[plugin]["group"][group_id] = True
            else:
                result[plugin] = False
        self.__dump()
        return result

    # 忽略插件
    def __ignore_plugin(self, plugins: Dict[str, bool]) -> "PluginList":
        for plugin in plugins:
            if plugin in self.__plugin_list:
                self.__plugin_list[plugin]["ignore"] = True
            else:
                self.__plugin_list[plugin] = {
                    "ignore": plugins[plugin],
                    "global": True,
                    "user": {},
                    "group": {},
                }
        return self

    # 取消忽略插件
    def __unignore_plugin(self, plugins: Dict[str, bool]) -> "PluginList":
        for plugin in plugins:
            if plugin in self.__plugin_list:
                self.__plugin_list[plugin]["ignore"] = plugins[plugin]
            else:
                self.__plugin_list[plugin] = {
                    "ignore": plugins[plugin],
                    "global": True,
                    "user": {},
                    "group": {},
                }
        return self

    # 添加插件（暂时不会用到）
    def __add_plugin(
        self,
        plugins: List[str],
    ) -> "PluginList":
        for plugin in plugins:
            if plugin not in self.__plugin_list:
                self.__plugin_list[plugin] = {
                    "ignore": plugins[plugin],
                    "global": True,
                    "user": {},
                    "group": {},
                }
        return self

    # 移除插件（暂时不会用到）
    def __remove_plugin(
        self,
        plugins: List[str],
    ) -> "PluginList":
        for plugin in plugins:
            if plugin in self.__plugin_list:
                self.__plugin_list.pop(plugin)
        return self

    # 加载插件列表
    def __load(self) -> Dict[str, Dict[str, Union[bool, Dict[int, bool]]]]:
        try:
            self.__plugin_list = yaml.safe_load(self.__path.open("r", encoding="utf-8"))
        except FileNotFoundError:
            self.__plugin_list = {}
        return self

    # 保存插件列表
    def __dump(self):
        self.__path.parent.mkdir(parents=True, exist_ok=True)
        yaml.dump(
            self.__plugin_list,
            self.__path.open("w", encoding="utf-8"),
            allow_unicode=True,
        )
