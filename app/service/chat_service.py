import traceback
from typing import List

from domain.model.chat import Chat, ChatType
from app.utils.result_wrapper import *
from data.repository.message_repository import MessageRepository
from data.repository.user_repository import UserRepository
from domain.model.group import Group
from domain.model.user import User
from fastapi import Depends, HTTPException
from data.repository.chat_repository import ChatRepository
from data.repository.group_repository import GroupRepository
from app.model.response.chat import Chat as ResponseChat


class ChatService:
    def __init__(
        self,
        user_repository: UserRepository = Depends(),
        message_repository: MessageRepository = Depends(),
        chat_repository: ChatRepository = Depends(),
        group_repository: GroupRepository = Depends()
    ):
        self.user_repository = user_repository
        self.message_repository = message_repository
        self.chat_repository = chat_repository
        self.group_repository = group_repository

    async def get_recent_chats(
        self, user_self: User
    ) -> ResultWrapper[List[ResponseChat]]:
        try:
            chat_objs = await self.chat_repository.get_all_chats_for_user(user_self.id)
            print(chat_objs)

            chats: List[ResponseChat] = list()

            for chat_obj in chat_objs:

                if chat_obj.last_message_id:
                    last_message = await self.message_repository.get_message_by_id(chat_obj.last_message_id)
                else:
                    last_message = None

                if chat_obj.type == ChatType.one_to_one.value:
                    remote_user_id = [
                        id for id in chat_obj.user_ids if id != user_self.id
                    ][0]

                    remote_user = await self.user_repository.get_user_by_id(remote_user_id)
                
                    chat = ResponseChat(
                        chat_obj.id,
                        chat_obj.type,
                        remote_user.name,
                        [user_self, remote_user],
                        None,
                        remote_user.profile_image_url,
                        last_message
                    )
                    chats.append(chat)

                elif chat_obj.type == ChatType.group.value:
                    users: List[User] = list()
                    group = await self.group_repository.get_group_by_id(chat_obj.group_id)

                    if not group:
                        continue

                    for user_id in group.user_ids:
                        user = await self.user_repository.get_user_by_id(user_id)
                        users.append(user)
  
                    chat = Chat(
                        chat_obj.id,
                        chat_obj.type,
                        group.name,
                        users,
                        group.id,
                        group.profile_image_url,
                        last_message
                    )
                    chats.append(chat)
            return chats

        except Exception as e:
            print(traceback.print_exc())
            return Error()

    async def create_new_chat(
        self, current_user: User, remote_user_id: str
    ) -> ResultWrapper[str]:
        try:
            return await self.chat_repository.create_new_one_to_one_chat(
                current_user.id, remote_user_id
            )
        except Exception as e:
            print(traceback.format_exc())
            return Error()

    async def get_chat_by_id(self, chat_id: str) -> ResultWrapper[Chat]:
        try:
            return await self.chat_repository.get_chat_by_id(chat_id)
        except:
            traceback.print_exc()
            return Error()

    async def update_last_message(self, message_id: str, chat_id: str):
        try:
            await self.chat_repository.update_last_message(chat_id, message_id)
        except:
            print(traceback.format_exc())
