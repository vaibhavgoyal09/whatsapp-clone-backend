from data.repository.message_repository import MessageRepository
from fastapi import Depends, HTTPException
from fastapi.responses import ORJSONResponse
import traceback
from app.utils.result_wrapper import *
from app.model.message import Message 


class MessageService:

    def __init__(self, message_repository: MessageRepository = Depends()):
        self.message_repository = message_repository

    async def get_messages_for_chat(self, chat_id: int, page: int, page_size: int) -> ResultWrapper[list]:
        try:
            messages = await self.message_repository.get_messages_for_chat(
                page=page,
                page_size=page_size,
                chat_id=chat_id
            )

            return Success[list[Message]](messages)
        except:
            print(traceback.print_exc())
            return []
