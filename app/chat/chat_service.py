from fastapi import Depends, HTTPException
from typing import List


class ChatService:

    def __init__(self):
        pass

    async def create_new_chat():
        pass

    async def get_all_chats():
        pass


def get_chat_service():
    return ChatService()