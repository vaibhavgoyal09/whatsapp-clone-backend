from dataclasses import dataclass, asdict
from typing import Union, List
from enum import Enum


class ChatType(Enum):
    one_to_one = 0
    group = 1


@dataclass
class Chat:
    id: str
    user_ids: List[str]
    type: int = ChatType.one_to_one.value
    unseen_message_count: int = 0
    last_message_id: Union[str, None] = None
