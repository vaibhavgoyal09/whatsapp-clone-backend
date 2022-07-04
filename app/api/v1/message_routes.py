from fastapi import Depends, APIRouter
from app.service.message_service import MessageService


router = APIRouter(prefix='/message', tags=['message'])


@router.get('/{chat_id}')
async def get_messages_for_chat(
    chat_id: int,
    page: int = 0,
    page_size=20,
    message_service: MessageService = Depends()
):
    return await message_service.handle_get_messages_for_chat(
        chat_id=chat_id,
        page=page,
        page_size=page_size
    )
