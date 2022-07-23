import dataclasses
from enum import Enum
from typing import Union
from datetime import datetime


class MessageType(Enum):
    text = 0
    audio = 1
    video = 2
    gif = 3


@dataclasses.dataclass
class Message:
    id: int
    type: int
    message: str
    sender_id: str
    chat_id: str
    media_url: Union[str, None]
    created_at: int