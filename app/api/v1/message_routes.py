from fastapi import Depends, APIRouter, HTTPException
from app.service.message_service import MessageService
from app.utils.result_wrapper import *
from fastapi.responses import ORJSONResponse

router = APIRouter(prefix="/message", tags=["message"])


@router.get("/{chat_id}")
async def get_messages_for_chat(
    chat_id: str,
    page: int = 0,
    page_size=20,
    message_service: MessageService = Depends(),
):
    result: ResultWrapper = await message_service.get_messages_for_chat(
        chat_id=chat_id, page=page, page_size=page_size
    )
    if isinstance(result, Error):
        raise HTTPException(result.code, detail=result.message)
    else:
        return ORJSONResponse(result)
