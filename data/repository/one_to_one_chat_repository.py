from typing import List

from app.model.user import User
from data.database import get_session
from data.model.one_to_one_chat import OneToOneChatTable
from data.model.user import UserTable
from fastapi import Depends
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Union


class OneToOneChatRepository:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.db_session: AsyncSession = session

    async def create_new_chat(self, users: List[UserTable]) -> str:
        chat = OneToOneChatTable(last_message_id=None, users=users)
        self.db_session.add(chat)
        await self.db_session.commit()
        await self.db_session.refresh(chat)

        return chat.id

    async def get_chat_by_id(self, chat_id: str) -> OneToOneChatTable:
        query = select(OneToOneChatTable).where(OneToOneChatTable.id == chat_id)
        result = await self.db_session.execute(query)
        return result.first().OneToOneChatTable

    # async def get_chat_id_where_users(self, user_ids: List[int]) -> Union[str, None]:
    #     query = (
    #         select(ChatTable.id.label("id"))
    #         .join(user_chat, user_chat.c.chat_id == ChatTable.id)
    #         .where(and_(user_chat.c.user_id.in_([user_ids[0]]), user_chat.c.user_id.in_([user_ids[1]])))
    #     )
    #     result = await self.db_session.execute(query)
    #     return result.first().id
        
    async def get_all_chats_for_user(self, user_self: User) -> List[OneToOneChatTable]:
        query = (
            select(OneToOneChatTable)
            .where(OneToOneChatTable.user_id == user_self.id)
        )

        results = await self.db_session.execute(query)
        chats: List[ChatTable] = []

        for result in results:
            result = result.ChatTable
            chats.append(result)

        return chats

    async def update_last_message(self, chat_id: int, last_message_id: int):
        chat_obj = await self.get_chat_by_id(chat_id)
        chat_obj.last_message_id = last_message_id
        await self.db_session.flush()
        await self.db_session.commit()
