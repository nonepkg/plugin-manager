from typing import Annotated

from nonebot.params import Depends
from nonebot_plugin_session import SessionId, EventSession, SessionLevel, SessionIdType


def _realm_id(session: EventSession) -> str:
    if session.level == SessionLevel.GROUP:
        realm_id = f"{session.platform}:{session.id2}"
    elif session.level == SessionLevel.CHANNEL:
        realm_id = f"{session.platform}:{session.id3}_{session.id2}"
    else:
        realm_id = ""
    return realm_id


def _platform(session: EventSession) -> str:
    return session.platform


Platform = Annotated[str, Depends(_platform)]
UserId = Annotated[
    str,
    SessionId(
        SessionIdType.USER, include_bot_type=False, include_bot_id=False, seperator=":"
    ),
]
RealmId = Annotated[str, Depends(_realm_id)]
