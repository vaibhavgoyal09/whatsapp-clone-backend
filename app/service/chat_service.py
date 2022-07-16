import traceback
from typing import List

from app.model.user import User
from app.utils.result_wrapper import *
from data.repository.one_to_one_chat_repository import OneToOneChatRepository
from data.repository.user_repository import UserRepository
from data.repository.group_repository import GroupRepository
from fastapi import Depends, HTTPException
from app.model.chat import Chat
from app.model.response.chats_groups_response import ChatGroupResponse, ChatGroupType
from app.model.group import Group


class ChatService:
    def __init__(
        self,
        one_to_one_chat_repository: OneToOneChatRepository = Depends(),
        user_repository: UserRepository = Depends(),
        group_repository: GroupRepository = Depends()
    ):
        self.one_to_one_chat_repository = one_to_one_chat_repository
        self.user_repository = user_repository
        self.group_repository = group_repository

    async def get_all_chats(self, user_self: User) -> ResultWrapper[List[ChatGroupResponse]]:
        try:
            chats_objs = await self.one_to_one_chat_repository.get_all_chats_for_user(user_self)
            group_objs = await self.group_repository.get_groups_for_user(user_id=user_self.id)

            chats: List[Chat] = list()
            groups: List[Group] = list()

            for chat_obj in chats_objs:
                remote_user = self.user_repository.get_raw_user_by_id(chat_obj.remote_user_id)
                chat = Chat(
                    id=chat_obj.id,
                    remote_user_id=remote_user.id,
                    remote_user_name=remote_user.name,
                    remote_user_profile_image_url=remote_user.profile_image_url,
                )
                chats.append(chat)
   
            for group_obj in group_objs:
                pass

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
                current_user = await self.user_repository.get_raw_user_by_id(
                    current_user.id
                )
                remote_user = await self.user_repository.get_raw_user_by_id(
                    remote_user_id
                )
                return await self.one_to_one_chat_repository.create_new_chat(
                    users=[current_user, remote_user]
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
