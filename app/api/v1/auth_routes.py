from fastapi import APIRouter, Depends
from app.model.request.register_user import RegisterUser
from app.auth.auth_service import AuthService


router = APIRouter(prefix='/auth', tags=["auth"])


@router.post('/register')
async def register_user(
    request: RegisterUser,
    auth_service: AuthService = Depends()
):
    return await auth_service.handle_add_user(request)