from dataclasses import dataclass
from typing import Union
from app.model.message import MessageType


@dataclass
class WsMessage:
   to_id: int
   chat_id: int
   text: Union[str, None] = None
   media_url: Union[str, None] = None
   type: int = MessageType.text.value
