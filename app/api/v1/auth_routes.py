from fastapi import APIRouter, Depends
from app.model.request.register_user import RegisterUser
from app.auth.auth_service import AuthService
from app.model.user import User
from app.auth.firebase_service import get_current_user_uid


router = APIRouter(prefix='/auth', tags=["auth"])


@router.post('/register')
async def register_user(
    request: RegisterUser,
    user_firebase_uid: str = Depends(get_current_user_uid),
    auth_service: AuthService = Depends()
):
    return await auth_service.handle_add_user(request, user_firebase_uid)