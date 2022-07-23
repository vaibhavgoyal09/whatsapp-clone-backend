from dataclasses import dataclass
from typing import Union
from domain.model.message import MessageType
from app.model.add_message_request import AddMessageRequest
from enum import Enum


class WsMessageType(Enum):
   message = 0
   audio_call = 1
   video_call = 2


@dataclass
class WsMessage:
   type: int
   message: Union[AddMessageRequest]
