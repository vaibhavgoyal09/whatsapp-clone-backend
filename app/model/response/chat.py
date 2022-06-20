from dataclasses import dataclass
from typing import Optional


class Chat:
    id: int
    remote_user_id: int
    remote_user_profile_image_url: str
    remote_user_name: str
    last_message: Optional[str]
    unseen_message_count: int = 0