from data.model.chat import ChatTable
from typing import List
from app.model.user import User
from fastapi import Depends
from app.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, join
from data.model.user import UserTable
from data.model.relations.user_chat import user_chat


class ChatRepository:

    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.db_session: AsyncSession = session

    async def create_new_chat(
        self,
        users: List[User],
        message_id: str
    ):
        chat = ChatTable(
            last_message_id=message_id,
            users=users
        )

        await self.db_session.add(chat)
        await self.db_session.commit()

    async def get_all_chats_for_user(self, user_self: User) -> List[ChatTable]:
        query = select(ChatTable).join(user_chat, user_chat.c.chat_id ==
                               ChatTable.id).where(user_chat.c.user_id == user_self.id)

        print(query)

        results = await self.db_session.execute(query)

        for result in results:
            print(result.ChatTable.id, result.ChatTable.unseen_message_count)