from dataclasses import dataclass
from typing import Union, List
from domain.model.message import Message


@dataclass
class Chat:
    id: str
    type: int
    name: str
    user_ids: List[str]
    group_id: Union[str, None] = None
    profile_image_url: Union[str, None] = None
    last_message: Union[Message, None] = None
