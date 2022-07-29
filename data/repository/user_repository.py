import traceback
from typing import List, Optional, Union

from app.model.request.register_user import RegisterUser
from app.model.request.update_user_request import UpdateUserRequest
from domain.model.user import User, OnlineStatusType
from bson.objectid import ObjectId
from data.database import CollectionNames, get_database
from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorDatabase
from datetime import datetime


class UserRepository:
    def __init__(self, database: AsyncIOMotorDatabase = Depends(get_database)):
        self.user_collection: AsyncIOMotorCollection = database[
            CollectionNames.USER_COLLECTION.value
        ]

    async def add_user(
        self,
        name: str,
        firebase_uid: str,
        about: str,
        profile_image_url: str,
        phone_number: str,
    ) -> str:
        user = {
            "name": name,
            "firebase_uid": firebase_uid,
            "profile_image_url": profile_image_url,
            "about": about,
            "phone_number": phone_number,
            "online_status": OnlineStatusType.online.value,
            "last_online_at": int(datetime.timestamp(datetime.now()) * 1000)
        }

        result = await self.user_collection.insert_one(user)
        return str(result.inserted_id)

    async def get_user_by_id(self, user_id: str) -> Union[User, None]:
        result = await self.user_collection.find_one({"_id": ObjectId(user_id)})
        return User.from_db_model(result)

    async def get_user_by_firebase_uid(self, firebase_uid: str) -> Union[User, None]:
        result = await self.user_collection.find_one({"firebase_uid": firebase_uid})
        if result:
            return User.from_db_model(result)
        else:
            return None

    async def get_user_by_phone_number(self, phone_number: str) -> Union[User, None]:
        result = await self.user_collection.find_one({"phone_number": phone_number})
        if result:
            return User.from_db_model(result)
        else:
            return None

    async def search_users_by_phone_number(
        self, user_self_id: int, query_value: str
    ) -> List[User]:
        cursor = self.user_collection.find(
                {"$and": [{"phone_number": {"$regex": query_value.replace("+", "")}}, { "_id": {"$ne": ObjectId(user_self_id)} }]}
        )

        users: List[User] = list()

        async for document in cursor:
            users.append(User.from_db_model(document))
        return users

    async def search_users_by_name(
        self, user_self_id: int, query_value: str
    ) -> List[User]:
        cursor = self.user_collection.find(
                { "$and": [{"name": {"$regex": query_value.replace("+", "")}}, {"_id": {"$ne": ObjectId(user_self_id)}}]}
        )

        users: List[User] = list()

        async for document in cursor:
            users.append(User.from_db_model(document))
        return users

    async def update_user_details(self, user_uid: str, request: UpdateUserRequest):
        updated_user = dict()

        if request.name:
            updated_user["name"] = request.name
        if request.about:
            updated_user["about"] = request.about
        if request.profile_image_url or request.should_remove_profile_photo:
            updated_user["profile_image_url"] = request.profile_image_url

        await self.user_collection.update_one(
            {"firebase_uid": user_uid}, {"$set": updated_user}
        )

    async def update_user_online_status(self, user_id: str, status_type: int):
        updates = dict()
        updates["online_status"] = status_type
        if status_type == OnlineStatusType.offline.value:
            updates["last_online_at"] = int(datetime.timestamp(datetime.now()) * 1000)

        await self.user_collection.update_one(
            {"_id": ObjectId(user_id)}, {"$set": updates}
        )
