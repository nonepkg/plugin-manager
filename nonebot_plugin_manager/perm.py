import json
from collections.abc import Iterable
from dataclasses import field, dataclass
from contextlib import asynccontextmanager

from anyio import Path
from arclet.cithun.ctx import Context
from arclet.cithun.node import Node, NodeState
from arclet.cithun import User, Group, SyncMonitor


class DefaultMonitor(SyncMonitor):
    def __init__(self, file: Path):
        if not file.suffix.startswith(".json"):
            raise ValueError(file)
        self.file = file
        self.USER_TABLE: dict[str, DefaultUser] = {}
        self.GROUP_TABLE: dict[str, DefaultGroup] = {}

    def new_group(self, name: str, priority: int):
        if name in self.GROUP_TABLE:
            raise ValueError(f"Group {name} already exists")
        group = DefaultGroup(name, priority)
        self.GROUP_TABLE[name] = group
        return group

    def get_group(self, name: str, priority: int, *groups: Group):
        if name in self.GROUP_TABLE:
            return self.GROUP_TABLE[name]
        group = DefaultGroup(name, priority)
        self.GROUP_TABLE[name] = group
        self.group_inherit(group, *groups)
        return group

    def new_user(self, name: str):
        if name in self.USER_TABLE:
            raise ValueError(f"User {name} already exists")
        user = DefaultUser(name)
        self.USER_TABLE[name] = user
        return user

    def get_user(self, name: str, *groups: Group):
        if name in self.USER_TABLE:
            return self.USER_TABLE[name]
        user = DefaultUser(name)
        self.USER_TABLE[name] = user
        self.user_inherit(user, *groups)
        return user

    async def load(self):
        if await self.file.exists():
            async with await self.file.open("r", encoding="utf-8") as f:
                data = json.loads(await f.read())
            users = {
                name: DefaultUser.parse(raw) for name, raw in data["users"].items()
            }
            groups = {
                name: DefaultGroup.parse(raw) for name, raw in data["groups"].items()
            }
            self.USER_TABLE.update(users)
            self.GROUP_TABLE.update(groups)
            for group in groups.values():
                group.inherits = [self.GROUP_TABLE[gp.name] for gp in group.inherits]
            for user in users.values():
                user.inherits = [self.GROUP_TABLE[gp.name] for gp in user.inherits]
            del users, groups
        else:
            await self.save()

    async def save(self):
        data = {
            "users": {user.name: user.dump() for user in self.USER_TABLE.values()},
            "groups": {group.name: group.dump() for group in self.GROUP_TABLE.values()},
        }
        async with await self.file.open("w", encoding="utf-8") as f:
            await f.write(json.dumps(data, ensure_ascii=False, indent=2))

    def group_inherit(self, target: Group, *groups: Group):
        for group in groups:
            if group not in target.inherits:
                target.inherits.append(group)

    def user_inherit(self, target: User, *groups: Group):
        for group in groups:
            if group not in target.inherits:
                target.inherits.append(group)

    def user_leave(self, target: User, group: Group):
        if group in target.inherits:
            target.inherits.remove(group)

    @asynccontextmanager
    async def transaction(self):
        yield
        await self.save()

    def all_users(self) -> Iterable[User]:
        return self.USER_TABLE.values()

    def all_groups(self) -> Iterable[Group]:
        return self.GROUP_TABLE.values()


@dataclass(eq=True, unsafe_hash=True)
class DefaultGroup:
    name: str
    priority: int
    nodes: dict[Node, dict[Context, NodeState]] = field(
        default_factory=dict, compare=False, hash=False
    )
    inherits: list = field(default_factory=list, compare=False, hash=False)

    def dump(self):
        return {
            "name": self.name,
            "priority": self.priority,
            "nodes": {
                str(node): {str(ctx): state.state for ctx, state in data.items()}
                for node, data in self.nodes.items()
            },
            "inherits": [gp.name for gp in self.inherits],
        }

    @classmethod
    def parse(cls, raw: dict):
        obj = cls(raw["name"], raw["priority"])
        obj.nodes = {
            Node(node): {
                Context.from_string(ctx): NodeState(state)
                for ctx, state in data.items()
            }
            for node, data in raw["nodes"].items()
        }
        for node in obj.nodes:
            if not node.exists():
                node.touch()
        obj.inherits = [DefaultGroup(name, 0) for name in raw["inherits"]]
        return obj

    def __str__(self):
        return f"Group({self.name})"


@dataclass(eq=True, unsafe_hash=True)
class DefaultUser:
    name: str
    nodes: dict[Node, dict[Context, NodeState]] = field(
        default_factory=dict, compare=False, hash=False
    )
    inherits: list = field(default_factory=list, compare=False, hash=False)

    def dump(self):
        return {
            "name": self.name,
            "nodes": {
                str(node): {str(ctx): state.state for ctx, state in data.items()}
                for node, data in self.nodes.items()
            },
            "inherits": [user.name for user in self.inherits],
        }

    @classmethod
    def parse(cls, raw: dict):
        obj = cls(raw["name"])
        obj.nodes = {
            Node(node): {
                Context.from_string(ctx): NodeState(state)
                for ctx, state in data.items()
            }
            for node, data in raw["nodes"].items()
        }
        for node in obj.nodes:
            if node.exists():
                node.touch()
        obj.inherits = [DefaultUser(name) for name in raw["inherits"]]
        return obj

    def __str__(self):
        return f"User({self.name})"
