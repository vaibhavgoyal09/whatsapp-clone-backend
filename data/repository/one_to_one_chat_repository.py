from typing import List

from app.model.user import User
from fastapi import Depends
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Union


class OneToOneChatRepository:
    async def create_new_chat(self, user_self_id: int, remote_user_id: int) -> str:
        pass

    async def get_chat_by_id(self, chat_id: str):
        pass

    # async def get_chat_id_where_users(self, user_ids: List[int]) -> Union[str, None]:
    #     query = (
    #         select(ChatTable.id.label("id"))
    #         .join(user_chat, user_chat.c.chat_id == ChatTable.id)
    #         .where(and_(user_chat.c.user_id.in_([user_ids[0]]), user_chat.c.user_id.in_([user_ids[1]])))
    #     )
    #     result = await self.db_session.execute(query)
    #     return result.first().id

    async def get_all_chats_for_user(self, user_self: User):
        pass

    async def update_last_message(self, chat_id: int, last_message_id: int):
        pass
