from fastapi import APIRouter, Depends, HTTPException
from app.model.request.register_user import RegisterUser
from app.service.user_service import UserService
from app.service.firebase_service import get_current_user_uid, get_current_user
from app.utils.result_wrapper import *
from fastapi.responses import ORJSONResponse
from app.model.user import User
from app.model.request.update_user_request import UpdateUserRequest


router = APIRouter(prefix="/user", tags=["user"])


@router.get("/current")
async def get_current_user_details(user: User = Depends(get_current_user)):
    return ORJSONResponse(user)


@router.get("/details/{user_id}")
async def get_user_details(user_id: int, service: UserService = Depends()):
    result: ResultWrapper = await service.get_user_details(user_id)
    if isinstance(result, Error):
        raise HTTPException(status_code=result.code, detail=result.message)
    else:
        return ORJSONResponse(result)


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


@router.get("/check_exists/{phone_number}")
async def check_if_user_exists(phone_number: str, service: UserService = Depends()):
    result = await service.check_if_user_exists(phone_number)
    if isinstance(result, Error):
        raise HTTPException(result.code, detail=result.message)
    return ORJSONResponse(result)


@router.get("/search/phone")
async def search_users_by_phone_number(
    phone_number: str,
    service: UserService = Depends(),
    user: User = Depends(get_current_user),
):
    result = await service.search_users_by_phone_number(
        user_self=user, query_value=phone_number
    )
    if isinstance(result, Error):
        raise HTTPException(result.code, detail=result.message)

    return ORJSONResponse(result)


@router.get("/search/name")
async def search_contacts_by_name(
    name: str,
    service: UserService = Depends(),
    user: User = Depends(get_current_user),
):
    result = await service.search_users_by_name(
        user_self=user, query_value=name
    )
    if isinstance(result, Error):
        raise HTTPException(result.code, detail=result.message)

    return ORJSONResponse(result)


@router.put("/update")
async def update_user_details(
    request: UpdateUserRequest,
    user_uid: str = Depends(get_current_user_uid),
    service: UserService = Depends(),
):
    result = await service.update_user_details(user_uid, request)
    if isinstance(result, Error):
        raise HTTPException(result.code, detail=result.message)
