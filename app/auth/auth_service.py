from data.repository.user_repository import UserRepository
from app.model.user import User
from app.model.request.register_user import RegisterUser
from fastapi import Depends, HTTPException, status
import traceback


class AuthService:

    def __init__(self, repository: UserRepository):
        self.user_repository = repository

    async def get_user_by_firebase_uid(self, firebase_uid: int) -> User:
        try:
            return await self.user_repository.get_user_by_firebase_uid(firebase_uid)
        except:
            print(traceback.format_exc())
            return None

    async def add_user(self, request: RegisterUser):
        try:
            self.user_repository.add_user(
                name=request.name,
                firebase_uid=request.firebase_uid,
                about=request.about,
                profile_image_url=request.profile_image_url,
                phone_number=request.phone_number)
        except:
            print(traceback.format_exc())
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="An unknown error occurred"
            )


def get_auth_service(repository: UserRepository = Depends()) -> AuthService:
    return AuthService(repository)
