from pydantic import BaseModel


class RegisterUser(BaseModel):
    name: str
    about: str
    phone_number: str
    profile_image_url: str