from typing import Dict
from fastapi import WebSocket, Depends
from app.model.ws_message import WsMessage
from app.model.message import Message
from app.service.chat_service import ChatService
from app.service.message_service import MessageService
from app.model.add_message_request import AddMessageRequest
from app.utils.result_wrapper import *
import orjson


class ChatController:
    def __init__(
        self,
        chat_service: ChatService = Depends(),
        message_service: MessageService = Depends(),
    ):
        self.online_users: Dict[int, WebSocket] = dict()
        self.chat_service: ChatService = chat_service
        self.message_service: MessageService = message_service

    async def connect(self, user_id: int, websocket: WebSocket):
        await websocket.accept()
        self.online_users[user_id] = websocket

    def disconnect(self, user_id: int):
        self.online_users.pop(user_id)

    async def send_message(self, own_user_id: int, ws_message: WsMessage):
        add_message_result: ResultWrapper = await self.message_service.add_message(
            request=AddMessageRequest(
                type=ws_message.type,
                media_url=ws_message.media_url,
                text=ws_message.text,
                own_user_id=own_user_id,
                chat_id=ws_message.chat_id,
            )
        )
        if isinstance(add_message_result, Error):
            return
        else:
            message = add_message_result

        if not self.online_users[own_user_id] or not self.online_users[ws_message.to_id]:
            print("Either User Was null")
            return
        # elif not self.online_users[ws_message.to_id]  // TODO("Send FCM Push Notification")
        await self.online_users[own_user_id].send_text(orjson.dumps(message))
        await self.online_users[ws_message.to_id].send_text(orjson.dumps(message))

        await self.chat_service.update_last_message(message_id=message.id)
