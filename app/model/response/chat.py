from dataclasses import dataclass
from typing import Union, List
from domain.model.message import Message
from domain.model.user import User


@dataclass
class Chat:
   id: int
   type: int
   name: str
   users: List[User]
   group_id: Union[str, None] = None
   profile_image_url: Union[str, None] = None
   last_message: Union[Message, None] = None