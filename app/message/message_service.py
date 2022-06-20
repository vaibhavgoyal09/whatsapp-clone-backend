from data.repository.message_repository import MessageRepository
from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
import traceback


class MessageService:

    def __init__(self, message_repository: MessageRepository = Depends()):
        self.message_repository = message_repository

    async def handle_get_messages_for_chat(self, chat_id: int, page: int, page_size: int):
        try:
            messages = await self.message_repository.get_messages_for_chat(
                page=page,
                page_size=page_size,
                chat_id=chat_id
            )

            return ORJSONResponse(messages)
        except:
            print(traceback.print_exc())
            return []
