from app.utils.result_wrapper import *
from app.model.request.create_group_request import CreateGroupRequest
from domain.model.group import Group
from domain.model.user import User
from app.model.response.group import Group as ResponseGroup
from fastapi import Depends
from data.repository.group_repository import GroupRepository
from data.repository.chat_repository import ChatRepository
from data.repository.user_repository import UserRepository
from typing import List
import traceback
from app.model.response.chat import Chat
from domain.model.chat import ChatType


class GroupService:
    def __init__(
        self,
        group_repository: GroupRepository = Depends(),
        chat_repository: ChatRepository = Depends(),
        user_repository: UserRepository = Depends(),
    ):
        self.group_repository = group_repository
        self.chat_repository = chat_repository
        self.user_repository = user_repository

    async def create_group(
        self, request: CreateGroupRequest, user_self: User
    ) -> ResultWrapper[Chat]:
        try:
            user_ids = request.user_ids
            if len(user_ids) < 1:
                raise AttributeError("Users Can't Be Empty")
            user_ids.append(user_self.id)
            group_id = await self.group_repository.create_group(
                user_self_id=user_self.id,
                name=request.name,
                user_ids=user_ids,
                profile_image_url=request.profile_image_url,
            )
            chat_id = await self.chat_repository.create_new_group_chat(
                group_id, user_ids
            )
            chat = await self.chat_repository.get_chat_by_id(chat_id)

            return Chat(
                id=chat.id,
                name=request.name,
                profile_image_url=request.profile_image_url,
                type=ChatType.group.value,
                group_id=group_id,
                user_ids=user_ids,
                last_message=None,
            )
        except:
            traceback.print_exc()
            return Error()

    async def get_group_details(self, group_id: str) -> ResultWrapper[ResponseGroup]:
        try:
            group = await self.group_repository.get_group_by_id(group_id)
            if not group:
                raise Exception(f"Group With ID:{group_id} Not Found")
            users: List[User] = list()

            for user_id in group.user_ids:
                user = await self.user_repository.get_user_by_id(user_id)
                if not user:
                    continue
                users.append(user)

            return ResponseGroup(
                group.id, group.name, users, group.profile_image_url, group.admin_id
            )
        except:
            traceback.print_exc()
            return Error()

    async def add_participants(self, group_id: str, user_ids: List[str]) -> ResultWrapper[None]:
        try:
            await self.group_repository.add_participants(group_id, user_ids)
            await self.chat_repository.add_participants(group_id, user_ids)
        except:
            traceback.print_exc()
            return Error()

    async def remove_participants(self, group_id: str, user_ids: List[str]) -> ResultWrapper[None]:
        try:
            await self.group_repository.remove_participants(group_id, user_ids)
            await self.chat_repository.remove_participants(group_id, user_ids)
        except:
            traceback.print_exc()
            return Error()