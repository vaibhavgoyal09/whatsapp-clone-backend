from typing import List

from domain.model.user import User
from fastapi import Depends
from typing import Union


class OneToOneChatRepository:
    async def create_new_chat(self, user_self_id: int, remote_user_id: int) -> str:
        pass

    async def get_chat_by_id(self, chat_id: str):
        pass

    async def get_all_chats_for_user(self, user_self: User):
        pass

    async def update_last_message(self, chat_id: int, last_message_id: int):
        pass
