import traceback
from typing import List

from app.model.user import User
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import asc, desc, and_
from app.model.request.update_user_request import UpdateUserRequest
from sqlalchemy.exc import NoResultFound


class UserRepository:
    async def add_user(
        self,
        name: str,
        firebase_uid: str,
        about: str,
        profile_image_url: str,
        phone_number: str,
    ) -> str:
        pass

    async def get_user_by_firebase_uid(self, firebase_uid: str) -> User:
        pass

    async def get_raw_user_by_firebase_uid(self, firebase_uid: str):
        pass

    async def get_raw_user_by_id(self, user_id: int):
        pass

    async def get_user_by_phone_number(self, phone_number) -> User:
        pass

    async def search_users_by_phone_number(
        self, user_self_id: int, query_value: str
    ) -> List[User]:
        pass

    async def search_users_by_name(
        self, user_self_id: int, query_value: str
    ) -> List[User]:
        pass

    async def update_user_details(self, user_uid: str, request: UpdateUserRequest):
        pass
