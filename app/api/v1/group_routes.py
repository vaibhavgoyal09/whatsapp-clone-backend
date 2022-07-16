from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import ORJSONResponse
from app.service.firebase_service import get_current_user
from app.model.request.create_group_request import CreateGroupRequest
from app.service.group_service import GroupService
from app.utils.result_wrapper import *
from app.model.user import User


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
