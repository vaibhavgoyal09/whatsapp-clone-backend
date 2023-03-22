from dataclasses import dataclass
from typing import Union
from app.model.incoming_call import IncomingCall
from app.model.add_message_request import AddMessageRequest
from app.model.typing_status import TypingStatus
from enum import Enum


class WsMessageType(Enum):
   message = 0
   typing_status = 1
   incoming_call = 2
   incoming_call_response = 3
   calling_event = 4


@dataclass
class WsMessage:
   type: int
   message: Union[AddMessageRequest, TypingStatus, IncomingCall]
