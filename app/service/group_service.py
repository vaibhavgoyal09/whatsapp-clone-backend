from app.utils.result_wrapper import *
from app.model.request.create_group_request import CreateGroupRequest
from app.model.user import User
from fastapi import Depends
from data.repository.group_repository import GroupRepository
from data.repository.user_repository import UserRepository
from data.model.user import UserTable
from typing import List


class GroupService:
    def __init__(
        self,
        group_repository: GroupRepository = Depends(),
        user_repository: UserRepository = Depends(),
    ):
        self.group_repository = group_repository
        self.user_repository = user_repository

    async def create_group(
        self, request: CreateGroupRequest, user_self: User
    ) -> ResultWrapper[int]:
        try:
            users: List[UserTable] = list()
            if len(request.user_ids) < 1:
                raise AttributeError("Users Can't Be Empty")
            for user_id in request.user_ids:
                users.append(self.user_repository.get_raw_user_by_id(user_id))
            return await self.group_repository.create_group(
                user_self_id=user_self.id,
                name=request.name,
                users=users,
                description=request.description,
                profile_image_url=request.profile_image_url,
            )
        except:
            return Error()
