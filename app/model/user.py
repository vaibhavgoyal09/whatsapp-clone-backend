from dataclasses import dataclass
import orjson
from fastapi.responses import ORJSONResponse


@dataclass
class User:
    id: int
    firebase_uid: str
    name: str
    about: str
    phone_number: str
    profile_image_url: str


    @staticmethod
    def toJson(user):
        return orjson.dumps(user)
