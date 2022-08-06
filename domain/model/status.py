from dataclasses import dataclass
from enum import Enum


class StatusType(Enum):
    image = 0
    video = 1


@dataclass
class Status:
    id: str
    user_id: str
    type: int
    media_url: str
    created_at: int

    @staticmethod
    def from_db_model(db_model):
        return Status(
            id=str(db_model.get("_id")),
            user_id=db_model.get("user_id"),
            type=db_model.get("type"),
            media_url=db_model.get("media_url"),
            created_at=db_model.get("created_at"),
        )
