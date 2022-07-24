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
    group_id: Union[str, None] = None
    last_message_id: Union[str, None] = None

    @staticmethod
    def from_db_model(db_model):
        return Chat(
            str(db_model.get("_id")),
            group_id=db_model.get("group_id"),
            user_ids=db_model.get("user_ids"),
            type=db_model.get("type"),
            last_message_id=db_model.get("last_message_id"),
        )
