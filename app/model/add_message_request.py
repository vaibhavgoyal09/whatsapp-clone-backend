from dataclasses import dataclass
from typing import Union, Dict


@dataclass
class AddMessageRequest:
   type: int
   own_user_id: str
   to_user_id: str
   chat_id: str
   media_url: Union[str, None] = None
   text: Union[str, None] = None

   @staticmethod
   def from_dict(request_dict: Dict, own_user_id: str):
      return AddMessageRequest(
         type=request_dict["type"],
         own_user_id=own_user_id,
         to_user_id=request_dict["to_user_id"],
         chat_id=request_dict["chat_id"],
         media_url=request_dict["media_url"],
         text=request_dict["text"]
      )
