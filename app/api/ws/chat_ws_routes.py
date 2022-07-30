from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from app.api.ws.chat_controller import ChatController, get_chat_controller
import orjson
from app.service.firebase_service import get_current_user
from domain.model.user import User
from app.model.ws_message import WsMessageType
from typing import Dict
from app.model.add_message_request import AddMessageRequest
import traceback
from app.model.typing_status import TypingStatus


router = APIRouter(prefix="/chat", tags=["chat_websocket"])


@router.websocket("/{client_id}")
async def messaging_websocket_route(
    websocket: WebSocket,
    client_id: str,
    controller: ChatController = Depends(get_chat_controller)
):
    await controller.connect(user_id=client_id, websocket=websocket)
    print(f"{client_id} connected successfully")
    try:
        while True:
            received_text = await websocket.receive_text()
            payload: Dict = orjson.loads(received_text)
            if payload["type"] == WsMessageType.message.value:
                message = AddMessageRequest.from_dict(payload["message"], client_id)
                await controller.send_message(client_id, message)
            elif payload["type"] == WsMessageType.typing_status.value:
                status = TypingStatus.from_dict(payload["message"])
                await controller.send_user_typing_status_change(client_id, status)
    except WebSocketDisconnect:
        print(traceback.format_exc())
        await controller.disconnect(client_id)
