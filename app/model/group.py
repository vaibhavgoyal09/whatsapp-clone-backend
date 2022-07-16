from dataclasses import dataclass
from typing import Union, List


@dataclass
class Group:
    id: int
    name: str
    description: Union[str, None] = None
    profile_image_url: Union[str, None] = None
