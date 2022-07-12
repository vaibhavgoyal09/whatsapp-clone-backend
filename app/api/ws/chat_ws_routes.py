from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from app.api.ws.chat_controller import ChatController
import orjson
from app.service.firebase_service import get_current_user
from app.model.user import User

router = APIRouter(prefix="/chat", tags=["chat_websocket"])


@router.websocket("/")
async def messaging_websocket_route(
    websocket: WebSocket,
    client_id: str,
    # current_user: User = Depends(get_current_user),
    controller: ChatController = Depends(),
):
    await controller.connect(user_id=client_id, websocket=websocket)
    print(f'{client_id} connected successfully')
    try:
        while True:
            received_text = await websocket.receive_text()
            payload = orjson.loads(received_text)
            controller.send_message(client_id, payload)
    except WebSocketDisconnect:
        controller.disconnect(user_id)
