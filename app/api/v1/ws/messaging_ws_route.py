from fastapi import APIRouter, Depends, WebSocket


router = APIRouter(prefix='/ws', tags=['chat_websocket'])


@router.websocket('/chat/{chat_id}')
async def messaging_websocket_route(websocket: WebSocket, chat_id: str):
   pass