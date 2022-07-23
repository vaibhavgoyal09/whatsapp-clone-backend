from dataclasses import dataclass
from typing import Union
from domain.model.message import Message


@dataclass
class Chat:
   id: int
   type: int
   name: str
   unseen_message_count: int = 0
   profile_image_url: Union[str, None] = None
   last_message: Union[Message, None] = None