import traceback
from typing import List

from app.model.response.chat import Chat
from app.model.user import User
from app.utils.result_wrapper import *
from data.repository.chat_repository import ChatRepository
from fastapi import Depends, HTTPException


class ChatService:
    def __init__(self, chat_repository: ChatRepository = Depends()):
        self.chat_repository = chat_repository

    async def get_all_chats(self, user_self: User) -> ResultWrapper[List[Chat]]:
        try:
            chats_objs = await self.chat_repository.get_all_chats_for_user(user_self)

            chats: List[Chat] = []

            for chat_obj in chats_objs:
                users = await self.chat_repository.get_all_users_for_chat(
                    chat_obj.id
                )

                if len(users) > 2:
                    raise Exception("Users can't be more than two.")

                for user in users:
                    if user.id == user_self.id:
                        continue
                    else:
                        remote_user = user

                chat = Chat(
                    id=chat_obj.id,
                    remote_user_id=remote_user.id,
                    remote_user_name=remote_user.name,
                    remote_user_profile_image_url=remote_user.profile_image_url,
                    last_message_id=chat_obj.last_message_id,
                    unseen_message_count=chat_obj.unseen_message_count,
                )

                chats.append(chat)
            return chats

        except Exception as e:
            print(traceback.print_exc())
            return Error(message='Something Went Wrong')
