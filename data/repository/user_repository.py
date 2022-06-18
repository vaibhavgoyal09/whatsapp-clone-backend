from data.model.user import UserTable
from app.model.user import User
from fastapi import Depends
from app.database import get_session
from sqlalchemy.future import select


class UserRepository:

    def __init__(self, session=Depends(get_session)):
        self.db_session = session

    async def add_user(
        self,
        name: str,
        firebase_uid: str,
        about: str,
        profile_image_url: str,
        phone_number: str
    ):
        pass

    async def get_user_by_firebase_uid(self, firebase_uid: int) ->User :
        query = select(UserTable).where(UserTable.firebase_uid == firebase_uid)

        users = await self.db_session.execute(query)
        return users.scalars().one()

    async def update_user(
        self
    ):
        pass
