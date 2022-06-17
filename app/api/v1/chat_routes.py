from fastapi import APIRouter, Depends
from app.chat.chat_service import ChatService, get_chat_service
from app.auth.firebase_service import get_current_user
from domain.model.user import User


router = APIRouter(prefix='/chat', tags=['chat'])


@router.post('/new')
async def create_new_chat(
    service: ChatService = Depends(get_chat_service),
    user_self: User = Depends(get_current_user)
):
    pass


@router.get('/all')
async def get_all_chats(
    other_user_id: str,
    service: ChatService = Depends(get_chat_service),
    user: User = Depends(get_current_user)
):
    pass