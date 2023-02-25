from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from fastapi import Depends
from app.core.config import Settings, get_settings
from enum import Enum


class Database:
    client: AsyncIOMotorClient = None


db = Database()


class CollectionNames(Enum):
    USER_COLLECTION = "users"
    CHAT_COLLECTION = "chats"
    MESSAGE_COLLECTION = "messages"
    GROUP_COLLECTION = "groups"
    STATUS_COLLECTION = "statuses"


async def get_database(
    settings: Settings = Depends(get_settings),
) -> AsyncIOMotorDatabase:
    return db.client[settings.MONGO_DATABASE_NAME]


def connect_to_mongo():
    db.client = AsyncIOMotorClient(
        str(get_settings().DATABASE_URI),
        maxPoolSize=get_settings().MAX_CONNECTIONS_COUNT,
        minPoolSize=get_settings().MIN_CONNECTIONS_COUNT,
    )


def close_mongo_connection():
    if db.client:
        db.client.close()
