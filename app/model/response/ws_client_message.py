from dataclasses import dataclass
from typing import Union
from app.model.response.incoming_call_response_client import IncomingCallResponseClient
from app.model.response.typing_status_change import TypingStatusChange
from domain.model.message import Message
from app.model.incoming_call_client import IncomingCallClient


@dataclass
class WsClientMessage:
    type: int
    message: Union[Message, TypingStatusChange, IncomingCallClient, IncomingCallResponseClient]
