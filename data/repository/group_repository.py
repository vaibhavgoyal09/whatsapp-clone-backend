from typing import Optional, List
from fastapi import Depends
from data.database import get_database, CollectionNames
from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorCollection
from bson.objectid import ObjectId
from domain.model.group import Group


class GroupRepository:
    def __init__(self, database: AsyncIOMotorDatabase = Depends(get_database)):
        self.group_collection = database[CollectionNames.GROUP_COLLECTION.value]
    
    async def create_group(
        self,
        user_self_id: int,
        name: str,
        # users: List[UserTable],
        description: Optional[str] = None,
        profile_image_url: Optional[str] = None,
    ) -> int:
        # group_obj = GroupTable(
        #     name=name,
        #     admin_id=user_self_id,
        #     description=description,
        #     profile_image_url=profile_image_url,
        #     users=users,
        # )
        # self.db_session.add(group_obj)

        # try:
        #     await self.db_session.commit()
        #     await self.db_session.refresh(group_obj)
        #     return group_obj.id
        # except Exception as e:
        #     await self.db_session.rollback()
        #     raise e
        pass

    async def get_group_by_id(self, group_id: str) -> Group:
        result = await self.group_collection.find_one({"_id": ObjectId(group_id)})

    async def get_groups_for_user(self, user_id: int):
        # query = (
        #     select(GroupTable)
        #     .join(user_group, user_group.c.group_id == GroupTable.id)
        #     .where(user_group.c.user_id == user_id)
        # )
        # resulted_rows = await self.db_session.execute(query)
        # groups: List[GroupTable] = list()

        # for row in resulted_rows:
        #     group_obj = row.GroupTable
        #     groups.append(group_obj)
            
        # return groups
        pass
