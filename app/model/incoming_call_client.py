from dataclasses import dataclass
from typing import Optional


@dataclass
class IncomingCallClient:
    call_type: str
    user_id: str
    user_name: str
    user_profile_image_url: Optional[str]
