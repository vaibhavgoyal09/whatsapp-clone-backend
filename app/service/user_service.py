import traceback
from typing import List, Union

from app.model.request.register_user import RegisterUser
from app.model.request.update_user_request import UpdateUserRequest
from app.model.response.register_user_response import RegisterUserResponse
from app.model.user import User
from app.utils.result_wrapper import *
from data.repository.user_repository import UserRepository
from fastapi import Depends


class UserService:
    def __init__(self, repository: UserRepository = Depends()):
        self.user_repository = repository

    async def get_user_by_firebase_uid(self, firebase_uid: int) -> Union[User, None]:
        try:
            return await self.user_repository.get_user_by_firebase_uid(firebase_uid)
        except:
            print(traceback.format_exc())
            return None

    async def get_user_details(self, user_id: str) -> ResultWrapper[User]:
        try:
            user = await self.user_repository.get_user_by_id(user_id)
            if not user:
                raise Exception("No user found")
            else:
                return user
        except:
            print(traceback.format_exc())
            return Error(message="No user found")

    async def add_user(
        self, request: RegisterUser, user_firebase_uid: str
    ) -> ResultWrapper[RegisterUserResponse]:
        try:
            user = await self.get_user_by_phone_number(request.phone_number)
            if user:
                return Error(
                    message=f"User with phone number {request.phone_number} already exists"
                )
            user_id = await self.user_repository.add_user(
                about=request.about,
                name=request.name,
                firebase_uid=user_firebase_uid,
                profile_image_url=request.profile_image_url,
                phone_number=request.phone_number,
            )
            return RegisterUserResponse(user_id)
        except Exception as e:
            print(traceback.format_exc())
            return Error(message="Something Went Wrong")

    async def get_user_by_phone_number(self, phone_number: str) -> Union[User, None]:
        try:
            return await self.user_repository.get_user_by_phone_number(phone_number)
        except:
            return None

    async def check_if_user_exists(self, phone_number: str) -> ResultWrapper[bool]:
        try:
            user = await self.get_user_by_phone_number(phone_number)
            return user != None
        except Exception as e:
            print(traceback.format_exc())
            return Error(message="Something Went Wrong")

    async def search_users_by_phone_number(
        self, user_self: User, query_value: str
    ) -> ResultWrapper[List[User]]:
        try:
            result = await self.user_repository.search_users_by_phone_number(
                user_self_id=user_self.id, query_value=query_value.replace(" ", "")
            )
            return result
        except Exception as e:
            print(traceback.format_exc())
            return Error(message="Something Went Wrong")

    async def search_users_by_name(
        self, user_self: User, query_value: str
    ) -> ResultWrapper[List[User]]:
        try:
            result = await self.user_repository.search_users_by_name(
                user_self_id=user_self.id, query_value=query_value.replace(" ", "")
            )
            return result
        except Exception as e:
            print(traceback.format_exc())
            return Error(message="Something Went Wrong")

    async def update_user_details(
        self, user_uid: str, request: UpdateUserRequest
    ) -> ResultWrapper[None]:
        try:
            return await self.user_repository.update_user_details(user_uid, request)
        except:
            print(traceback.format_exc())
            return Error(message="Something Went Wrong")
