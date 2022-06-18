from fastapi import Depends, HTTPException
from typing import List
from data.repository.chat_repository import ChatRepository
from app.model.user import User
import traceback
from app.model.response.chat import Chat


class ChatService:

    def __init__(self, chat_repository: ChatRepository = Depends()):
        self.chat_repository = chat_repository

    async def handle_get_all_chats(self, user_self: User):
        try:
            chats_objs = await self.chat_repository.get_all_chats_for_user(user_self)

            # for chat_obj in chats_objs:

            #     remote_user = chat_obj.users.

            #     chat_response = Chat(

            #     )

        except:
            print(traceback.print_exc())
            return []