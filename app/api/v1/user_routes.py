from fastapi import APIRouter, Depends, HTTPException
from app.model.request.register_user import RegisterUser
from app.user.user_service import UserService
from app.model.user import User
from app.user.firebase_service import get_current_user_uid
from app.utils.result_wrapper import *
from fastapi.responses import ORJSONResponse


router = APIRouter(prefix="/user", tags=["user"])


@router.post("/register")
async def register_user(
    request: RegisterUser,
    user_firebase_uid: str = Depends(get_current_user_uid),
    user_service: UserService = Depends(),
):
    result: ResultWrapper = await user_service.add_user(request, user_firebase_uid)
    print(result)
    if isinstance(result, Error):
        raise HTTPException(result.code, detail=result.message)
    else:
        return ORJSONResponse(result)


@router.get("/{phone_number}")
async def check_if_user_exists(phone_number: str, service: UserService = Depends()):
    result = await service.get_user_by_phone_number(phone_number)
    if isinstance(result, Error):
        raise HTTPException(result.code, detail=result.message)
    
    return ORJSONResponse(result)