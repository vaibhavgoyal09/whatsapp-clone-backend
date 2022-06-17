from data.model.user import UserTable
from app.model.user import User
from tortoise.expressions import Q


class UserRepository():

    async def add_user(
        self,
        name: str,
        firebase_uid: str,
        about: str,
        profile_image_url: str,
        phone_number: str
    ):
        await UserTable.create(
            UserTable(
                firebase_uid=firebase_uid,
                name=name,
                about=about,
                profile_image_url=profile_image_url,
                phone_number=phone_number
            )
        )

    async def get_user_by_firebase_uid(self, firebase_uid: int):
        user_obj = await UserTable.get(firebase_uid=firebase_uid)

        return User(
            id=user_obj.id,
            firebase_uid=user_obj.firebase_uid,
            name=user_obj.name,
            about=user_obj.about,
            profile_image_url=user_obj.profile_image_url,
            phone_number=user_obj.phone_number
        )

    async def update_user(
        self
    ):
        pass
