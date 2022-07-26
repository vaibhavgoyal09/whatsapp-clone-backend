from data.database import get_database, CollectionNames
from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorCollection
from fastapi import Depends
from domain.model.chat import Chat, ChatType
from typing import List
from bson.objectid import ObjectId


class ChatRepository:
		def __init__(self, database: AsyncIOMotorDatabase = Depends(get_database)):
			self.chat_collection: AsyncIOMotorCollection = database[
				CollectionNames.CHAT_COLLECTION.value
			]

		async def create_new_one_to_one_chat(
			self, user_self_id: str, remote_user_id: str
		) -> str:
			chat = {
				"user_ids": [user_self_id, remote_user_id],
				"group_id": None,
				"type": ChatType.one_to_one.value,
				"last_message_id": None,
			}
			result = await self.chat_collection.insert_one(chat)
			return str(result.inserted_id)

		async def create_new_group_chat(
			self, group_id: str, user_ids: List[str]
			) -> str:
			chat = {
				"user_ids": user_ids,
				"group_id": group_id,
				"type": ChatType.group.value,
				"last_message_id": None,
			}
			result = await self.chat_collection.insert_one(chat)
			return str(result.inserted_id)

		async def get_all_chats_for_user(self, user_id: str) -> List[Chat]:
			cursor = self.chat_collection.find({"user_ids": user_id})
			chats: List[Chat] = list()
			async for document in cursor:
				chats.append(Chat.from_db_model(document))

			return chats

		async def get_chat_by_id(self, chat_id: str) -> Chat:
			result = await self.chat_collection.find_one({"_id": ObjectId(chat_id)})
			if not result:
				raise Exception("No Chat Found")
			return Chat.from_db_model(result)

		async def update_last_message(self, chat_id: str, last_message_id: str):
			updated_chat = {"last_message_id": last_message_id}

			result = await self.chat_collection.update_one(
				{"_id": ObjectId(chat_id)}, {"$set": updated_chat}
			)
