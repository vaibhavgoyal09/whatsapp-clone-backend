from pydantic import BaseModel


class RegisterUser(BaseModel):
    firebase_uid: str
    name: str
    about: str
    phone_number: str
    profile_image_url: str