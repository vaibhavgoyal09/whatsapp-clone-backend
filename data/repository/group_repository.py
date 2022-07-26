from typing import Optional, List
from fastapi import Depends
from data.database import get_database, CollectionNames
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson.objectid import ObjectId
from domain.model.group import Group


class GroupRepository:
    def __init__(self, database: AsyncIOMotorDatabase = Depends(get_database)):
        self.group_collection = database[CollectionNames.GROUP_COLLECTION.value]
    
    async def create_group(
        self,
        user_self_id: str,
        name: str,
        user_ids: List[str],
        profile_image_url: Optional[str] = None,
    ) -> str:
        if not user_self_id in user_ids:
            user_ids.append(user_self_id)
        group = {
            "name": name,
            "user_ids": user_ids,
            "admin_id": user_self_id,
            "profile_image_url": profile_image_url
        }
        result = await self.group_collection.insert_one(group)
        return str(result.inserted_id)

    async def get_group_by_id(self, group_id: str) -> Group:
        result = await self.group_collection.find_one({"_id": ObjectId(group_id)})
        if not result:
            return None
        return Group.from_db_model(result)

    async def get_groups_for_user(self, user_id: str) -> List[Group]:
        cursor = self.group_collection.find({"user_ids": {"$in": [ObjectId(user_id)]}})
        groups: List[Group] = list()

        async for document in cursor:
            groups.append(Group.from_db_model(document))

        return groups
