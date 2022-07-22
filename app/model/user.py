from dataclasses import dataclass


@dataclass(eq=False)
class User:
    id: str
    firebase_uid: str
    name: str
    about: str
    phone_number: str
    profile_image_url: str

    def __eq__(self, other):
        try:
            return self.id == other.id
        except:
            return False

    @staticmethod
    def from_db_model(db_model):
        return User(
            id=str(db_model.get("_id")),
            firebase_uid=db_model.get("firebase_uid"),
            name=db_model.get("name"),
            about=db_model.get("about"),
            phone_number=db_model.get("phone_number"),
            profile_image_url=db_model.get("profile_image_url"),
        )
