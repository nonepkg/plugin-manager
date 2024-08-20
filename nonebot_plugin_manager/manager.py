from typing import Optional

from anyio import Path
from nonebot_plugin_localstore import get_config_dir
from arclet.cithun import PE, ROOT, Context, NodeState, context

from .perm import DefaultUser as User
from .perm import DefaultMonitor as Monitor

CONFIG_PATH = get_config_dir(None)


class PluginManager:
    _path: Path
    _monitor: Monitor

    def __init__(self):
        self._path = Path(CONFIG_PATH / "plugin_manager.json")
        self._monitor = Monitor(self._path)
        self.init_plugin("/")

    def _op_user(self, user_id: str, scope: str, enable: bool):
        context_data = {"scope": scope} if scope else {}
        with context(**context_data):
            PE.root.set(self.get_user(user_id), ROOT, NodeState("vma"), recursive=True)

    def get_user(self, user_id: str, bot_id: str = "", realm_id: str = "") -> User:
        user = self._monitor.get_user(user_id)
        if bot_id:
            bot = self._monitor.get_group(
                bot_id, 30, self._monitor.get_group("default", 10)
            )
            self._monitor.user_inherit(user, bot)
        if realm_id:
            realm = self._monitor.get_group(
                realm_id, 20, self._monitor.get_group("default", 10)
            )
            self._monitor.user_inherit(user, realm)
        return user

    def check_perm(self, plugin: str, user_id: str, realm_id: str, bot_id: str) -> bool:
        node = ROOT / plugin
        owner = self.get_user(user_id)
        with context(scope=bot_id):
            if (
                repr(Context(scope=bot_id))
                in (result := PE(owner).get(owner, node)).data
            ):
                return result.most.available
        with context(scope=realm_id):
            return PE(owner).get(owner, node).most.available

    def _able_plugin(
        self,
        plugin: str,
        executor_id: str,
        enable: bool,
        user_id: Optional[str] = None,
        realm_id: Optional[str] = None,
        scope: Optional[str] = None,
    ):
        node = ROOT / plugin
        if executor_id == "root":
            executor = PE.root
        else:
            executor = PE(self.get_user(executor_id))
        if realm_id:
            target = self._monitor.get_group(
                realm_id, 20, self._monitor.get_group("default", 10)
            )
        elif user_id:
            target = self.get_user(user_id)
        else:
            raise ValueError("user_id or realm_id must be provided")
        context_data = {"scope": scope} if scope else {}
        with context(**context_data):
            executor.set(
                target, node, NodeState("v-a" if enable else "v--"), recursive=True
            )

    def init_plugin(self, plugin: str):
        node = ROOT / plugin
        default = self._monitor.get_group("default", 10)
        if node in default.nodes:
            return
        node.touch(exist_ok=True)
        PE.root.set(default, node, NodeState("v-a"))


plugin_manager = PluginManager()
