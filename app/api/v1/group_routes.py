from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import ORJSONResponse
from app.service.firebase_service import get_current_user
from app.model.request.create_group_request import CreateGroupRequest
from app.model.request.add_participants_request import AddParticipantsRequest
from app.model.request.remove_participants_request import RemoveParticipantsRequest
from app.service.group_service import GroupService
from app.utils.result_wrapper import *
from domain.model.user import User


router = APIRouter(prefix="/group", tags=["group"])


@router.post("/new")
async def create_group(
    request: CreateGroupRequest,
    user: User = Depends(get_current_user),
    service: GroupService = Depends(),
):
    result: ResultWrapper = await service.create_group(request, user)
    if isinstance(result, Error):
        raise HTTPException(status_code=result.code, detail=result.message)
    return ORJSONResponse(result)


@router.get("/details/{group_id}")
async def get_group_details(
    group_id: str,
    user: User = Depends(get_current_user),
    service: GroupService = Depends(),
):
    result: ResultWrapper = await service.get_group_details(group_id)
    if isinstance(result, Error):
        raise HTTPException(result.code, detail=result.message)
    return ORJSONResponse(result)


@router.post("/participant/add")
async def add_participants(
    request: AddParticipantsRequest,
    user: User = Depends(get_current_user),
    service: GroupService = Depends(),
):
    result = await service.add_participants(request.group_id, request.user_ids)

    if isinstance(result, Error):
        raise HTTPException(result.code, detail=result.message)
    else:
        return ORJSONResponse(result)


@router.post("/participant/remove")
async def remove_participants(
    request: RemoveParticipantsRequest,
    user: User = Depends(get_current_user),
    service: GroupService = Depends(),
):
    result = await service.remove_participants(request.group_id, request.user_ids)

    if isinstance(result, Error):
        raise HTTPException(result.code, detail=result.message)
    else:
        return ORJSONResponse(result)
