from dataclasses import dataclass
from app.model.message import Message


@dataclass
class Chat:
    id: int
    remote_user_id: int
    remote_user_profile_image_url: str
    remote_user_name: str
