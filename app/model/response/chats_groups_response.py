from dataclasses import dataclass
from typing import Union
from app.model.chat import Chat
from app.model.group import Group
from app.model.message import Message
from enum import Enum


class ChatGroupType(Enum):
   one_to_one = 0
   group = 1


@dataclass
class ChatGroupResponse:
   type: int
   last_message: Union[Message, None] = None
   chat: Union[Chat, None] = None
   group: Union[Group, None] = None