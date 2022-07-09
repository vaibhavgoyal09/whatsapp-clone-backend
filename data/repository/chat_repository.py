from typing import List

from app.model.user import User
from data.database import get_session
from data.model.chat import ChatTable
from data.model.relations.user_chat import user_chat
from data.model.user import UserTable
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class ChatRepository:

    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.db_session: AsyncSession = session

    async def create_new_chat(
        self,
        users: List[User]
    ) -> str:
        chat = ChatTable(
            last_message_id=None,
            users=users
        )

        await self.db_session.add(chat)
        await self.db_session.commit()
        await self.db_session.refresh(chat)

        return chat.id

    async def get_chat_by_id(self, chat_id: str) -> ChatTable:
        query = select(ChatTable).where(ChatTable.id == chat_id)
        return await self.db_session.execute(query).one().ChatTable

    async def get_all_chats_for_user(self, user_self: User) -> List[ChatTable]:
        query = select(ChatTable).\
                join(user_chat, user_chat.c.chat_id == ChatTable.id).\
                where(user_chat.c.user_id == user_self.id)

        results = await self.db_session.execute(query)
        chats: List[ChatTable] = []

        for result in results:
            result = result.ChatTable
            chats.append(result)

        return chats

    async def get_all_users_for_chat(self, chat_id: int) -> List[UserTable]:
        query = select(UserTable).\
                join(user_chat, user_chat.c.user_id == UserTable.id).\
                where(user_chat.c.chat_id == chat_id)

        results = await self.db_session.execute(query)
        users: List[UserTable] = []

        for result in results:
            result = result.UserTable
            users.append(result)

        return users
