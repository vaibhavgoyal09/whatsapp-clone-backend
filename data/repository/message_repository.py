from typing import List, Optional

from app.model.message import Message, MessageType
from data.database import get_session
from data.model.message import MessageTable
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.model.add_message_request import AddMessageRequest


class MessageRepository:
    def __init__(self, db_session: AsyncSession = Depends(get_session)):
        self.db_session = db_session

    async def add_message(
        self,
        request: AddMessageRequest
    ) -> Message:
        message_obj = MessageTable(
            message=request.text,
            media_url=request.media_url,
            sender_id=request.own_user_id,
            chat_id=request.chat_id,
        )
        self.db_session.add(message_obj)
        await self.db_session.commit()
        await self.db_session.refresh(message_obj)

        print(message_obj)

        message = Message(
            id=message_obj.id,
            type=message_obj.type,
            message=message_obj.message,
            sender_id=message_obj.sender_id,
            chat_id=message_obj.chat_id,
            media_url=message_obj.media_url,
            created_at=message_obj.created_at,
        )
        return message

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
            # .offset(offset)
            # .limit(page_size)    // Currentlty not implemented pagination at Frontend 
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
