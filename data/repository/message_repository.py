from typing import List, Optional, Union

from domain.model.message import Message, MessageType
from fastapi import Depends
from app.model.add_message_request import AddMessageRequest
from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorCollection
from data.database import get_database, CollectionNames
from bson.objectid import ObjectId
from datetime import datetime
import pymongo


class MessageRepository:
    def __init__(self, database: AsyncIOMotorDatabase = Depends(get_database)):
        self.message_collection = database[CollectionNames.MESSAGE_COLLECTION.value]

    async def add_message(self, request: AddMessageRequest) -> str:
        message = {
            "type": request.type,
            "text": request.text,
            "sender_id": request.own_user_id,
            "chat_id": request.chat_id,
            "media_url": request.media_url,
            "created_at": int(datetime.timestamp(datetime.now()) * 1000),
        }
        result = await self.message_collection.insert_one(message)
        return str(result.inserted_id)

    async def get_messages_for_chat(
        self, page: int, page_size: int, chat_id: str
    ) -> List[Message]:
        cursor = (
            self.message_collection.find({"chat_id": chat_id})
            # .skip(page * page_size)
            # .limit(page_size)
            .sort("created_at", pymongo.DESCENDING)
        )
        messages: List[Message] = list()

        async for document in cursor:
            messages.append(Message.from_db_model(document))

        messages.reverse()
        return messages

    async def get_message_by_id(self, message_id: str) -> Union[Message, None]:
        result = await self.message_collection.find_one({"_id": ObjectId(message_id)})
        if result is None:
            return None
        else:
            return Message.from_db_model(result)
