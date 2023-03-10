import dataclasses
from enum import Enum
from typing import Union


class MessageType(Enum):
    text = 0
    audio = 1
    video = 2
    gif = 3


@dataclasses.dataclass
class Message:
    id: str
    type: int
    text: str
    sender_id: str
    chat_id: str
    media_url: Union[str, None]
    created_at: int

    @staticmethod
    def from_db_model(db_model):
        return Message(
            id=str(db_model.get("_id")),
            type=db_model.get("type"),
            text=db_model.get("text"),
            sender_id=db_model.get("sender_id"),
            chat_id=db_model.get("chat_id"),
            media_url=db_model.get("media_url"),
            created_at=db_model.get("created_at")
        )
