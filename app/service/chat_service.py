import traceback
from typing import List

from app.model.response.chat import Chat as ResponseChat
from app.utils.result_wrapper import *
from data.repository.message_repository import MessageRepository
from data.repository.user_repository import UserRepository
from domain.model.chat import Chat, ChatType
from domain.model.group import Group
from domain.model.user import User
from fastapi import Depends, HTTPException


class ChatService:
    def __init__(
        self,
        user_repository: UserRepository = Depends(),
        message_repository: MessageRepository = Depends()
    ):
        self.user_repository = user_repository
        self.message_repository = message_repository

    async def get_recent_chats(self, user_self: User) -> ResultWrapper[List[ResponseChat]]:
        try:
            return list()
        except Exception as e:
            print(traceback.print_exc())
            return Error()

    async def create_new_chat(
        self, current_user: User, remote_user_id: int
    ) -> ResultWrapper[str]:
        try:
           pass
        except Exception as e:
            print(traceback.format_exc())
            return Error()

    async def update_last_message(self, message_id: int, chat_id: int):
        try:
            pass
        except:
            print(traceback.format_exc())
