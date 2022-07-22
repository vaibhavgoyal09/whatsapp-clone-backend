from typing import List, Optional, Union

from app.model.message import Message, MessageType
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.model.add_message_request import AddMessageRequest


class MessageRepository:
    async def add_message(
        self,
        request: AddMessageRequest
    ) -> Message:
        pass

    async def get_messages_for_chat(
        self, page: int, page_size: int, chat_id: int
    ) -> List[Message]:
        pass

    async def get_message_by_id(self, message_id: int) -> Union[Message, None]:
        pass
