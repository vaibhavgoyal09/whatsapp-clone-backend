from fastapi import APIRouter, Depends
from app.model.request.register_user import RegisterUser
from app.auth.auth_service import AuthService, get_auth_service


router = APIRouter(prefix='/auth', tags=["auth"])


@router.post('/register')
async def register_user(
    request: RegisterUser,
    auth_service: AuthService = Depends(get_auth_service)
):
    await auth_service.add_user(request)