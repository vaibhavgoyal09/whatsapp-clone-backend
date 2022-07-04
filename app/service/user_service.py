from data.repository.user_repository import UserRepository
from app.model.user import User
from app.model.request.register_user import RegisterUser
from fastapi import Depends
import traceback
from app.utils.result_wrapper import *
from app.model.response.register_user_response import RegisterUserResponse


class UserService:
    def __init__(self, repository: UserRepository = Depends()):
        self.user_repository = repository

    async def get_user_by_firebase_uid(self, firebase_uid: int) -> User:
        try:
            return await self.user_repository.get_user_by_firebase_uid(firebase_uid)
        except:
            print(traceback.format_exc())
            return None

    async def add_user(
        self, request: RegisterUser, user_firebase_uid: str
    ) -> ResultWrapper[RegisterUserResponse]:
        try:
            user = await self.get_user_by_phone_number(request.phone_number)
            if user and isinstance(user, User):
                return Error(message=f'User with phone number {request.phone_number} already exists')
            user_id = await self.user_repository.add_user(
                name=request.name,
                firebase_uid=user_firebase_uid,
                about=request.about,
                profile_image_url=request.profile_image_url,
                phone_number=request.phone_number.replace(" ", ""),
            )
            return RegisterUserResponse(user_id)
        except Exception as e:
            print(traceback.format_exc())
            return Error(message='Something Went Wrong')

    async def get_user_by_phone_number(self, phone_number: str)-> ResultWrapper[User]:
        try:
            result = await self.user_repository.get_user_by_phone_number(phone_number.replace(" ", ""))
            if result is None:
                return Error(message='user not found')
            else:
                return result
        except Exception as e:
            print(traceback.format_exc())
            return Error(message='Something Went Wrong')