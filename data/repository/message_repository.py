from typing import List

from app.model.message import Message, MessageType
from data.database import get_session
from data.model.message import MessageTable
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class MessageRepository:
    def __init__(self, db_session: AsyncSession = Depends(get_session)):
        self.db_session = db_session

    async def get_messages_for_chat(
        self, page: int, page_size: int, chat_id: int
    ) -> List[Message]:

        if page < 0:
            raise AttributeError("page can't be less than 0.")

        if page == 0:
            offset = 0
        else:
            offset = page * page_size

        query = (
            select(MessageTable)
            .where(MessageTable.chat_id == chat_id)
            .order_by(MessageTable.created_at)
            .offset(offset)
            .limit(page_size)
        )

        result_rows = await self.db_session.execute(query)

        messages: List[Message] = []

        for row in result_rows:
            row = row.MessageTable

            message = Message(
                id=row.id,
                type=row.type,
                message=row.message,
                media_url=row.media_url,
                chat_id=row.chat_id,
                sender_id=row.sender_id,
                created_at=row.created_at,
            )

            messages.append(message)

        return messages
