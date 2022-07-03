from fastapi import APIRouter, Depends, HTTPException
from app.model.request.register_user import RegisterUser
from app.user.user_service import UserService
from app.model.user import User
from app.user.firebase_service import get_current_user_uid
from app.utils.result_wrapper import *
from fastapi.responses import ORJSONResponse


router = APIRouter(prefix='/user', tags=["user"])


@router.post('/register')
async def register_user(
    request: RegisterUser,
    user_firebase_uid: str = Depends(get_current_user_uid),
    auth_service: UserService = Depends()
):
    result: ResultWrapper = await auth_service.add_user(request, user_firebase_uid)
    print(result)
    if isinstance(result, Error):
        raise HTTPException(result.code, detail=result.message)
    else:
        return ORJSONResponse(result)
