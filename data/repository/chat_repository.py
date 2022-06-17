from data.model.chat import ChatTable, ChatType
from typing import List
from domain.model.user import User


class ChatRepository:

    async def create_new_chat(
        users: List[User]
    ):
        pass