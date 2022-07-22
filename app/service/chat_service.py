import traceback
from typing import List

from app.model.user import User
from app.utils.result_wrapper import *
from data.repository.one_to_one_chat_repository import OneToOneChatRepository
from data.repository.user_repository import UserRepository
from data.repository.group_repository import GroupRepository
from data.repository.message_repository import MessageRepository
from fastapi import Depends, HTTPException
from app.model.chat import Chat
from app.model.response.chat import Chat, ChatType
from app.model.group import Group


class ChatService:
    def __init__(
        self,
        one_to_one_chat_repository: OneToOneChatRepository = Depends(),
        user_repository: UserRepository = Depends(),
        group_repository: GroupRepository = Depends(),
        message_repository: MessageRepository = Depends()
    ):
        self.one_to_one_chat_repository = one_to_one_chat_repository
        self.user_repository = user_repository
        self.group_repository = group_repository
        self.message_repository = message_repository

    async def get_recent_chats(self, user_self: User) -> ResultWrapper[List[Chat]]:
        try:
            chats_objs = await self.one_to_one_chat_repository.get_all_chats_for_user(user_self)
            group_objs = await self.group_repository.get_groups_for_user(user_id=user_self.id)

            one_to_one_chats: List[Chat] = list()
            groups: List[Group] = list()

            for chat_obj in chats_objs:
                remote_user: UserTable = self.user_repository.get_raw_user_by_id(chat_obj.remote_user_id)
                if chat_obj.last_message_id:
                    last_message = await self.message_repository.get_message_by_id(chat_obj.last_message_id)
                else:
                    last_message = None
                chat = Chat(
                    chat_id=chat_obj.id,
                    type=ChatType.one_to_one.value,
                    name=remote_user.name,
                    profile_image_url=remote_user.profile_image_url,
                    last_message=last_message
                )
                chats.append(chat)
   
            for group_obj in group_objs:
                
                chat = Chat(
                    chat_id=group_obj.id,
                    type=ChatType.group.value,
                    name=group_obj.name,
                    profile_image_url=group_obj.profile_image_url,

                )

            # return chats
            return list()

        except Exception as e:
            print(traceback.print_exc())
            return Error(message="Something Went Wrong")

    async def create_new_chat(
        self, current_user: User, remote_user_id: int
    ) -> ResultWrapper[str]:
        try:
            # doesChatExists = await self.one_to_one_chat_repository.get_chat_id_where_users(
            #     user_ids=[current_user.id, remote_user_id]
            # )
            doesChatExists = False
            if doesChatExists:
                raise Exception("Chat Already exists")
            else:
                return await self.one_to_one_chat_repository.create_new_chat(
                    user_self_id=current_user.id, remote_user_id=remote_user_id
                )
        except Exception as e:
            print(traceback.format_exc())
            return Error(message="Something Went Wrong")

    async def update_last_message(self, message_id: int, chat_id: int):
        try:
            await self.one_to_one_chat_repository.update_last_message(
                last_message_id=message_id, chat_id=chat_id
            )
        except:
            print(traceback.format_exc())
