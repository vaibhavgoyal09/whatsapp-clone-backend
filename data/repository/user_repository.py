import traceback
from typing import List

from app.model.user import User
from data.database import get_session
from data.model.user import UserTable
from fastapi import Depends
from sqlalchemy.future import select
from sqlalchemy import asc, desc
from app.model.request.update_user_request import UpdateUserRequest


class UserRepository:
    def __init__(self, session=Depends(get_session)):
        self.db_session = session

    async def add_user(
        self,
        name: str,
        firebase_uid: str,
        about: str,
        profile_image_url: str,
        phone_number: str,
    ) -> str:
        user = UserTable(
            firebase_uid=firebase_uid,
            name=name,
            about=about,
            phone_number=phone_number,
            profile_image_url=profile_image_url,
        )
        self.db_session.add(user)

        try:
            await self.db_session.commit()
            await self.db_session.refresh(user)
            if user.id is None:
                print("User Id is None")
            else:
                print(user.id)
            return user.id
        except Exception as e:
            print(traceback.format_exc())
            await self.db_session.rollback()
            raise e

    async def get_user_by_firebase_uid(self, firebase_uid: str) -> User:
        user_table = await self.get_raw_user_by_firebase_uid(firebase_uid)
        return User(
            id=user_table.id,
            firebase_uid=user_table.firebase_uid,
            name=user_table.name,
            about=user_table.about,
            phone_number=user_table.phone_number,
            profile_image_url=user_table.profile_image_url,
        )

    async def get_raw_user_by_firebase_uid(self, firebase_uid: str) -> UserTable:
        query = select(UserTable).where(UserTable.firebase_uid == firebase_uid)
        users = await self.db_session.execute(query)
        return users.first().UserTable

    async def get_raw_user_by_id(self, user_id: int) -> UserTable:
        query = select(UserTable).where(UserTable.id == user_id)
        result = await self.db_session.execute(query)
        return result.first().UserTable

    async def get_user_by_phone_number(self, phone_number) -> User:

        query = select(UserTable).where(
            UserTable.phone_number.like(f"%{phone_number}%")
        )

        users = await self.db_session.execute(query)
        user_table_obj = users.first()

        if user_table_obj is None:
            raise Exception("User not found")

        user_table = user_table_obj.UserTable

        return User(
            id=user_table.id,
            firebase_uid=user_table.firebase_uid,
            name=user_table.name,
            about=user_table.about,
            phone_number=user_table.phone_number,
            profile_image_url=user_table.profile_image_url,
        )

    async def search_users_by_phone_number(self, query_value: str) -> List[User]:
        query = (
            select(UserTable)
            .where(UserTable.phone_number.like(f"%{query_value}%"))
            .order_by(asc(UserTable.phone_number))
        )

        users_obj = await self.db_session.execute(query)

        users: List[User] = []

        for user_obj in users_obj:
            user_obj = user_obj.UserTable
            user = User(
                id=user_obj.id,
                firebase_uid=user_obj.firebase_uid,
                name=user_obj.name,
                about=user_obj.about,
                phone_number=user_obj.phone_number,
                profile_image_url=user_obj.profile_image_url,
            )
            users.append(user)
        return users

    async def update_user_details(self, user_uid: str, request: UpdateUserRequest):
        user = await self.get_raw_user_by_firebase_uid(user_uid)

        if request.name:
            user.name = request.name
        if request.about:
            user.about = request.about
        if request.profile_image_url or request.should_remove_profile_photo:
            user.profile_image_url = request.profile_image_url

        await self.db_session.flush()
        await self.db_session.commit()
