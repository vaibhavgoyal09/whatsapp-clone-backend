from dataclasses import dataclass
from typing import List, Optional
from domain.model.user import User


@dataclass
class Group:
    id: str
    name: str
    users: List[User]
    profile_image_url: Optional[str]
    admin_id: str
