from dataclasses import dataclass
from typing import Union


@dataclass
class AddMessageRequest:
   type: int
   own_user_id: int
   chat_id: int
   media_url: Union[str, None] = None
   text: Union[str, None] = None