from dataclasses import dataclass
from typing import Union


@dataclass
class UpdateUserRequest:
   name: Union[str, None] = None
   about: Union[str, None] = None
   profile_image_url: Union[str, None] = None
   should_remove_profile_photo: bool = False