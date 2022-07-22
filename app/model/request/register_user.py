from dataclasses import dataclass, asdict

@dataclass
class RegisterUser:
    name: str
    about: str
    phone_number: str
    profile_image_url: str

    @staticmethod
    def as_dict(user):
        return asdict(user)