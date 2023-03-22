from fastapi import WebSocket, Depends
from app.model.calling_event_server import CallingEventServer
from app.model.incoming_call import IncomingCall
from app.model.response.calling_event_client import CallingEventClient
from app.model.response.incoming_call_response_client import IncomingCallResponseClient
from app.service.chat_service import ChatService
from app.service.message_service import MessageService
from app.service.user_service import UserService
from app.model.add_message_request import AddMessageRequest
from app.utils.result_wrapper import *
from functools import lru_cache
from app.api.ws.connection_manager import manager
from dataclasses import asdict
from domain.model.user import OnlineStatusType
from app.model.incoming_call import IncomingCall
from app.model.typing_status import TypingStatus
from app.model.response.typing_status_change import TypingStatusChange
from app.model.response.ws_client_message import WsClientMessage
from app.model.ws_message import WsMessageType
from app.model.incoming_call_client import IncomingCallClient
from app.model.incoming_call_response import IncomingCallResponse


class ChatController:
    def __init__(
        self,
        chat_service: ChatService,
        message_service: MessageService,
        user_service: UserService,
    ):
        self.chat_service: ChatService = chat_service
        self.message_service: MessageService = message_service
        self.user_service = user_service

    async def connect(self, user_id: str, websocket: WebSocket):
        await websocket.accept()
        manager.add_user(user_id, websocket)
        await self.user_service.update_user_online_status(
            user_id, OnlineStatusType.online.value
        )

    async def disconnect(self, user_id: str):
        manager.remove_user(user_id)
        await self.user_service.update_user_online_status(
            user_id, OnlineStatusType.offline.value
        )

    async def send_message(self, own_user_id: str, message_request: AddMessageRequest):
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

        chat = await self.chat_service.get_chat_by_id(message.chat_id)

        if isinstance(chat, Error):
            return

        client_message = WsClientMessage(
            type=WsMessageType.message.value, message=message
        )

        for user in chat.user_ids:
            socket = manager.get_websocket_for_user(user)
            if not socket:
                continue
            await socket.send_json(asdict(client_message))

    async def send_user_typing_status_change(
        self, user_self_id: str, status: TypingStatus
    ):
        chat = await self.chat_service.get_chat_by_id(status.chat_id)
        if isinstance(chat, Error):
            return
        message = TypingStatusChange(user_self_id, chat.id, status.is_typing)
        client_message = WsClientMessage(
            type=WsMessageType.typing_status.value, message=message
        )

        for user_id in chat.user_ids:
            if user_id == user_self_id:
                continue
            socket = manager.get_websocket_for_user(user_id)
            if not socket:
                continue
            await socket.send_json(asdict(client_message))

    async def send_incoming_call(self, call: IncomingCall):
        caller = await self.user_service.get_user_by_id(call.by_user_id)
        if not caller:
            return
        socket = manager.get_websocket_for_user(call.to_user_id)
        if not socket:
            return
        message = IncomingCallClient(
            call.call_type, caller.id, caller.name, caller.profile_image_url
        )
        client_message = WsClientMessage(WsMessageType.incoming_call.value, message)
        await socket.send_json(asdict(client_message))

    async def send_incoming_call_response(self, response: IncomingCallResponse):
        socket = manager.get_websocket_for_user(response.to_user_id)

        print(socket)

        if not socket:
            return

        client_message = WsClientMessage(
            WsMessageType.incoming_call_response.value,
            IncomingCallResponseClient(response.by_user_id, response.response),
        )

        await socket.send_json(asdict(client_message))

    async def handle_calling_event(self, user_self_id: str, event: CallingEventServer):
        socket = manager.get_websocket_for_user(event.to_user_id)

        if not socket:
            return

        client_message = WsClientMessage(
            WsMessageType.calling_event.value,
            CallingEventClient(user_self_id, event.event),
        )

        await socket.send_json(asdict(client_message))


@lru_cache
def get_chat_controller(
    message_service: MessageService = Depends(),
    chat_service: ChatService = Depends(),
    user_service: UserService = Depends(),
):
    return ChatController(
        message_service=message_service,
        chat_service=chat_service,
        user_service=user_service,
    )
