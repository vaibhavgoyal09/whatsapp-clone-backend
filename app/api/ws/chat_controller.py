from typing import Dict
from fastapi import WebSocket, Depends
from app.model.ws_message import WsMessage
from domain.model.message import Message
from app.service.chat_service import ChatService
from app.service.message_service import MessageService
from app.model.add_message_request import AddMessageRequest
from app.utils.result_wrapper import *
import orjson
from functools import lru_cache
from app.api.ws.connection_manager import manager
from dataclasses import asdict


class ChatController:
    def __init__(
        self,
        chat_service: ChatService,
        message_service: MessageService,
    ):
        print("Chat Controller Init Called.")
        self.chat_service: ChatService = chat_service
        self.message_service: MessageService = message_service

    async def connect(self, user_id: int, websocket: WebSocket):
        await websocket.accept()
        manager.add_user(user_id, websocket)
        print(manager.online_users)

    def disconnect(self, user_id: int):
        manager.remove_user(user_id)
        print(manager.online_users)

    async def send_message(self, own_user_id: int, message_request: AddMessageRequest):
        add_message_result: ResultWrapper = await self.message_service.add_message(
            request=message_request
        )
        if isinstance(add_message_result, Error):
            return
        else:
            message = add_message_result
        await self.chat_service.update_last_message(
            message_id=message.id, chat_id=message.chat_id
        )

        print(manager.online_users.keys())
        if not manager.get_websocket_for_user(
            own_user_id
        ) or not manager.get_websocket_for_user(message_request.to_user_id):
            print("Either User Was null")
            return
        # elif not self.online_users[ws_message.to_id]  // TODO("Send FCM Push Notification")
        print(f"Message is {message}")
        await manager.get_websocket_for_user(own_user_id).send_json(asdict(message))
        print(f"Serialize String Message is: {str(orjson.dumps(message))}")
        await manager.get_websocket_for_user(message_request.to_user_id).send_json(
            asdict(message)
        )


@lru_cache
def get_chat_controller(
    message_service: MessageService = Depends(), chat_service: ChatService = Depends()
):
    return ChatController(message_service=message_service, chat_service=chat_service)
