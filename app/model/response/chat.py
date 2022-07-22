from dataclasses import dataclass
from typing import Union
from app.model.message import Message
from enum import Enum


class ChatType(Enum):
   one_to_one = 0
   group = 1


@dataclass
class Chat:
   chat_id: int
   type: int
   name: str
   profile_image_url: Union[str, None] = None
   last_message: Union[Message, None] = None