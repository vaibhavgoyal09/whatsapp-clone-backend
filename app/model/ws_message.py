from dataclasses import dataclass
from typing import Union
from domain.model.message import MessageType
from app.model.add_message_request import AddMessageRequest
from app.model.typing_status import TypingStatus
from enum import Enum


class WsMessageType(Enum):
   message = 0
   typing_status = 1


@dataclass
class WsMessage:
   type: int
   message: Union[AddMessageRequest, TypingStatus]
