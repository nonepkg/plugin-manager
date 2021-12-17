import yaml
from pathlib import Path
from typing import Dict, List, Optional, Union

Conv = Dict[str, List[int]]


class PluginManager:
    __path: Path
    __plugin_list: Dict[str, Dict[str, Union[str, Dict[int, int]]]]

    def __init__(self, path: Path = Path() / "data" / "manager" / "plugin_list.yml"):
        self.__path = path
        self.__load()

    def get_plugin(
        self, conv: Conv = {"user": [], "group": []}, perm: Union[str, int] = 5
    ) -> Dict[str, bool]:
        """
        获取指定会话的插件列表

        参数:
            `conv: Conv` - 会话列表
            `perm: Union[str,int]` - 检测权限，满足该条件才返回 True

        返回:
            `Dict[str, bool]`
        """
        result = {}
        type = len(conv["user"]) + len(conv["group"])

        for p in self.__plugin_list:
            mode = int(self.__plugin_list[p]["mode"][type])
            for t in conv:
                can_break = False
                for i in conv[t]:
                    if i in self.__plugin_list[p][t]:
                        mode = int(self.__plugin_list[p][t][i])
                        if t == "user":
                            can_break = True
                if can_break:
                    break
            result[p] = True if mode & perm == perm else False
        pass
        return result

    # 设置插件模式
    def chmod_plugin(self, plugin: List[str], mode: str) -> Dict[str, bool]:
        result = {}
        for p in plugin:
            result[p] = False
            if p in self.__plugin_list:
                result[p] = True
                self.__plugin_list[p]["mode"] = mode
        self.__dump()
        return result

    # 禁用插件
    def block_plugin(
        self,
        plugin: List[str] = [],
        conv: Conv = {"user": [], "group": []},
    ) -> Dict[str, bool]:
        result = {}
        for p in plugin:
            result[p] = False
            if p in self.get_plugin():
                result[p] = True
                for t in conv:
                    for i in conv[t]:
                        if i in self.__plugin_list[p][t]:
                            mode = self.__plugin_list[p][t][i]
                        else:
                            mode = int(
                                self.__plugin_list[p]["mode"][1 if t == "user" else 2]
                            )
                        self.__plugin_list[p][t][i] = mode & 6

        self.__dump()
        return result

    # 启用插件
    def unblock_plugin(
        self,
        plugin: List[str] = [],
        conv: Conv = {"user": [], "group": []},
    ) -> Dict[str, bool]:
        result = {}
        for p in plugin:
            result[p] = False
            if p in self.get_plugin():
                result[p] = True
                for t in conv:
                    for i in conv[t]:
                        if i in self.__plugin_list[p][t]:
                            mode = self.__plugin_list[p][t][i]
                        else:
                            mode = int(
                                self.__plugin_list[p]["mode"][1 if t == "user" else 2]
                            )
                        self.__plugin_list[p][t][i] = mode | 1
        self.__dump()
        return result

    def update_plugin(self, plugin: Dict[str, bool]) -> "PluginManager":
        other = PluginManager().__add_plugin(plugin).__remove_plugin(plugin)
        self.__add_plugin(plugin).__remove_plugin(other.get_plugin(perm=4)).__dump()
        return self

    # 添加插件
    def __add_plugin(
        self,
        plugin: Dict[str, bool],
    ) -> "PluginManager":
        for p in plugin:
            if p not in self.__plugin_list:
                self.__plugin_list[p] = {
                    "mode": "755" if plugin[p] else "311",
                    "user": {},
                    "group": {},
                }
            elif plugin[p] ^ self.__plugin_list[p].get(
                "status",
                int(self.__plugin_list[p]["mode"][0]) & 4 == 4,
            ):
                self.__plugin_list[p]["mode"] = "".join(
                    str(int(m) | 4 if plugin[p] else int(m) & 3)
                    for m in self.__plugin_list[p]["mode"]
                )
            self.__plugin_list[p]["status"] = plugin[p]
        return self

    # 移除插件
    def __remove_plugin(
        self,
        plugin: Dict[str, bool],
    ) -> "PluginManager":
        new_plugin_list = {}
        for p in self.__plugin_list:
            if p not in plugin:
                new_plugin_list[p] = self.__plugin_list[p]
        self.__plugin_list = new_plugin_list
        return self

    # 加载插件列表
    def __load(self) -> "PluginManager":
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
