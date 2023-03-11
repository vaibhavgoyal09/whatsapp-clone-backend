from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from app.api.ws.chat_controller import ChatController, get_chat_controller
import orjson
from app.model.ws_message import WsMessageType
from app.model.incoming_call import IncomingCall
from typing import Dict
from app.model.add_message_request import AddMessageRequest
from app.model.typing_status import TypingStatus
from app.model.incoming_call_response import IncomingCallResponse


router = APIRouter(prefix="/chat", tags=["chat_websocket"])


@router.websocket("/{client_id}")
async def messaging_websocket_route(
    websocket: WebSocket,
    client_id: str,
    controller: ChatController = Depends(get_chat_controller)
):
    await controller.connect(user_id=client_id, websocket=websocket)
    try:
        while True:
            received_text = await websocket.receive_text()
            payload: Dict = orjson.loads(received_text)
            print(payload)
            if payload["type"] == WsMessageType.message.value:
                message = AddMessageRequest.from_dict(payload["message"], client_id)
                await controller.send_message(client_id, message)
            elif payload["type"] == WsMessageType.typing_status.value:
                status = TypingStatus.from_dict(payload["message"])
                await controller.send_user_typing_status_change(client_id, status)
            elif payload["type"] == WsMessageType.incoming_call.value:
                request = IncomingCall.from_dict(payload["message"])
                await controller.send_incoming_call(request)
            elif payload["type"] == WsMessageType.incoming_call_response.value:
                response = IncomingCallResponse.from_dict(payload["message"])
                await controller.send_incoming_call_response(response)

    except WebSocketDisconnect:
        await controller.disconnect(client_id)
