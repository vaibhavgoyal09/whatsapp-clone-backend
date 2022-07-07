from app.model.user import User
from app.service.chat_service import ChatService
from app.service.firebase_service import get_current_user
from app.utils.result_wrapper import *
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import ORJSONResponse

router = APIRouter(prefix="/chat", tags=["chat"])


@router.get("/all")
async def get_all_chats(
    service: ChatService = Depends(), user: User = Depends(get_current_user)
):
    result: ResultWrapper = await service.get_all_chats(user)
    if isinstance(result, Error):
        raise HTTPException(status_code=result.code, detail=result.message)
    else:
        return ORJSONResponse(result)
