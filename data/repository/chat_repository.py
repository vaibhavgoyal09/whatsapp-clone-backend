from data.database import get_database, CollectionNames
from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorCollection
from fastapi import Depends
from app.utils.result_wrapper import *


class ChatRepository:
	def __init__(self, database: AsyncIOMotorDatabase = Depends(get_database)):
		self.chat_collection: AsyncIOMotorCollection = database[
			CollectionNames.CHAT_COLLECTION.value
		]

	async def get_all_chats_for_user(self, user_id: str) -> ResultWrapper:
		pass