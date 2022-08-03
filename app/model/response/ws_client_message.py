from dataclasses import dataclass
from typing import Union
from app.model.response.typing_status_change import TypingStatusChange
from domain.model.message import Message


@dataclass
class WsClientMessage:
    type: int
    message: Union[Message, TypingStatusChange]
