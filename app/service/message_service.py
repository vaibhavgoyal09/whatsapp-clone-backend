import traceback
from typing import List

from domain.model.message import Message
from app.utils.result_wrapper import *
from data.repository.message_repository import MessageRepository
from fastapi import Depends
from app.model.add_message_request import AddMessageRequest


class MessageService:
    def __init__(self, message_repository: MessageRepository = Depends()):
        self.message_repository = message_repository

    async def get_messages_for_chat(
        self, chat_id: str, page: int, page_size: int
    ) -> ResultWrapper[List[Message]]:
        try:
            messages = await self.message_repository.get_messages_for_chat(
                page=page, page_size=page_size, chat_id=chat_id
            )

            return messages
        except:
            print(traceback.print_exc())
            return Error(message="Something Went Wrong")

    async def add_message(self, request: AddMessageRequest) -> ResultWrapper[Message]:
        try:
            message_id = await self.message_repository.add_message(request)
            message = await self.message_repository.get_message_by_id(message_id)
            if not message:
                raise Exception("Unexpected Error Occurred")
            return message
        except Exception:
            print(traceback.format_exc())
            return Error(message="Something Went Wrong")
