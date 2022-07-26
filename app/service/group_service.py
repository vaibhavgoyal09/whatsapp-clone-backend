from app.utils.result_wrapper import *
from app.model.request.create_group_request import CreateGroupRequest
from domain.model.user import User
from fastapi import Depends
from data.repository.group_repository import GroupRepository
from data.repository.chat_repository import ChatRepository
from typing import List
import traceback


class GroupService:
    def __init__(
        self,
        group_repository: GroupRepository = Depends(),
        chat_repository: ChatRepository = Depends()
    ):
        self.group_repository = group_repository
        self.chat_repository = chat_repository

    async def create_group(
        self, request: CreateGroupRequest, user_self: User
    ) -> ResultWrapper[int]:
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
            chat_id = await self.chat_repository.create_new_group_chat(group_id, user_ids)
            return chat_id
        except:
            traceback.print_exc()
            return Error()
