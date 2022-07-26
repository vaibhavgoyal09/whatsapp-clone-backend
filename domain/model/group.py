from dataclasses import dataclass
from typing import Union, List


@dataclass
class Group:
    id: int
    name: str
    user_ids: List[str]
    profile_image_url: Union[str, None] = None

    @staticmethod
    def from_db_model(db_model):
        return Group(
            id=str(db_model.get("_id")),
            name=db_model.get("name"),
            user_ids=db_model.get("user_ids"),
            profile_image_url=db_model.get("profile_image_url")
            )
