from data.model.group import GroupTable
from typing import Optional, List
from data.model.user import UserTable
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from data.model.relations.user_group import user_group
from sqlalchemy.future import select
from data.database import get_session


class GroupRepository:
    def __init__(self, db_session: AsyncSession = Depends(get_session)):
        self.db_session = db_session

    async def create_group(
        self,
        user_self_id: int,
        name: str,
        users: List[UserTable],
        description: Optional[str] = None,
        profile_image_url: Optional[str] = None,
    ) -> int:
        group_obj = GroupTable(
            name=name,
            admin_id=user_self_id,
            description=description,
            profile_image_url=profile_image_url,
            users=users,
        )
        self.db_session.add(group_obj)

        try:
            await self.db_session.commit()
            await self.db_session.refresh(group_obj)
            return group_obj.id
        except Exception as e:
            await self.db_session.rollback()
            raise e

    async def get_groups_for_user(self, user_id: int) -> List[GroupTable]:
        query = (
            select(GroupTable)
            .join(user_group, user_group.c.group_id == GroupTable.id)
            .where(user_group.c.user_id == user_id)
        )
        resulted_rows = await self.db_session.execute(query)
        groups: List[GroupTable] = list()

        for row in resulted_rows:
            group_obj = row.GroupTable
            groups.append(group_obj)
            
        return groups
