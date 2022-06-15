from dataclasses import dataclass

@dataclass
class User:
    id: int
    firebase_uid: str
    name: str
    about: str
    profile_image_url: str
    phone_number: str