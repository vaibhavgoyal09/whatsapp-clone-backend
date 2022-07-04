from fastapi import APIRouter, Depends
from app.service.chat_service import ChatService
from app.service.firebase_service import get_current_user
from app.model.user import User


router = APIRouter(prefix='/chat', tags=['chat'])


@router.get('/all')
async def get_all_chats(
    service: ChatService = Depends(),
    user: User = Depends(get_current_user)
):
    await service.handle_get_all_chats(user)