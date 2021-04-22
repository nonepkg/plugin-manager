import yaml
from pathlib import Path
from typing import Dict, List, Optional, Union


class PluginList:
    __path: Path
    __plugin_list: Dict[str, Dict[str, Union[str, Dict[int, bool]]]]

    def __init__(self, path: Path = Path() / "data" / "manager" / "plugin_list.yml"):
        self.__path = path
        self.__load()

    def get_plugins(
        self,
        mode: str = "",
        user_id: Optional[int] = None,
        group_id: Optional[int] = None,
    ) -> Dict[str, bool]:
        result = {}
        for plugin in self.__plugin_list:
            if (
                self.__plugin_list[plugin]["mode"][5:] != "-"
                or mode[len(mode) - 1 :] == "+"
            ):
                if (
                    mode[: len(mode) - 1] != "group"
                    and user_id in self.__plugin_list[plugin]["user"]
                ):
                    result[plugin] = self.__plugin_list[plugin]["user"][user_id]
                elif (
                    mode[: len(mode) - 1] != "user"
                    and group_id in self.__plugin_list[plugin]["group"]
                ):
                    result[plugin] = self.__plugin_list[plugin]["group"][group_id]
                else:
                    result[plugin] = (
                        True
                        if self.__plugin_list[plugin]["mode"][:5] == "black"
                        else False
                    )
            else:
                result[plugin] = False
        return result

    # 设置插件模式
    def set_plugin(self, plugins: List[str], mode: str) -> Dict[str, bool]:
        result = {}
        for plugin in plugins:
            if plugin in self.__plugin_list and self.get_plugins()[plugin]:
                result[plugin] = True
                self.__plugin_list[plugin]["mode"] = mode
            else:
                result[plugin] = False
        self.__dump()
        return result

    # 禁用插件
    def block_plugin(
        self,
        plugins: List[str],
        user_id: List[int] = [],
        group_id: List[int] = [],
        is_superuser: bool = False,
    ) -> Dict[str, bool]:
        conv = {"user": user_id, "group": group_id}
        result = {}
        for plugin in plugins:
            if plugin in self.__plugin_list and (
                is_superuser or self.__plugin_list[plugin]["mode"][5:] == "+"
            ):
                result[plugin] = True
                for type in conv:
                    for id in conv[type]:
                        self.__plugin_list[plugin][type][id] = False
            else:
                result[plugin] = False
        self.__dump()
        return result

    # 启用插件
    def unblock_plugin(
        self,
        plugins: List[str],
        user_id: List[int] = [],
        group_id: List[int] = [],
        is_superuser: bool = False,
    ) -> Dict[str, bool]:
        conv = {"user": user_id, "group": group_id}
        result = {}
        for plugin in plugins:
            if plugin in self.__plugin_list and (
                is_superuser or self.__plugin_list[plugin]["mode"][5:] == "+"
            ):
                result[plugin] = True
                for type in conv:
                    for id in conv[type]:
                        self.__plugin_list[plugin][type][id] = True
            else:
                result[plugin] = False
        self.__dump()
        return result

    def update_plugin(self, plugins: Dict[str, bool]) -> "PluginList":
        self.__add_plugin(plugins).__remove_plugin(plugins).__dump()
        return self

    # 添加插件
    def __add_plugin(
        self,
        plugins: Dict[str, bool],
    ) -> "PluginList":
        for plugin in plugins:
            if plugin not in self.__plugin_list:
                self.__plugin_list[plugin] = {
                    "mode": "black" if plugins[plugin] else "black-",
                    "user": {},
                    "group": {},
                }
            else:
                mode = self.__plugin_list[plugin]["mode"]
                if plugins[plugin]:
                    if mode[5:] != "+":
                        self.__plugin_list[plugin]["mode"] = mode[:5]
                else:
                    self.__plugin_list[plugin]["mode"] = mode[:5] + "-"
        return self

    # 移除插件
    def __remove_plugin(
        self,
        plugins: Dict[str, bool],
    ) -> "PluginList":
        for plugin in self.__plugin_list:
            if plugin not in plugins:
                self.__plugin_list[plugin]["mode"] = (
                    self.__plugin_list[plugin]["mode"][:5] + "-"
                )
            else:
                mode = self.__plugin_list[plugin]["mode"]
                if plugins[plugin]:
                    if mode[5:] != "+":
                        self.__plugin_list[plugin]["mode"] = mode[:5]
                else:
                    self.__plugin_list[plugin]["mode"] = mode[:5] + "-"
        return self

    # 加载插件列表
    def __load(self) -> Dict[str, Dict[str, Union[bool, Dict[int, bool]]]]:
        try:
            self.__plugin_list = yaml.safe_load(self.__path.open("r", encoding="utf-8"))
        except:
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
