from dataclasses import dataclass

@dataclass(eq=False)
class User:
    id: int
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