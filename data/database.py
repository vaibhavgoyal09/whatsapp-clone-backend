from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from fastapi import Depends
from app.core.config import Settings, get_settings
from enum import Enum


class Database:
    client: AsyncIOMotorClient = None

db = Database()


class CollectionNames(Enum):
    USER_COLLECTION = "users"


async def get_database(
    settings: Settings = Depends(get_settings),
) -> AsyncIOMotorDatabase:
    return db.client[settings.MONGO_DATABASE_NAME]


def connect_to_mongo():
    print("Initializing Database...")
    print(f"{str(get_settings().DATABASE_URI)}")
    db.client = AsyncIOMotorClient(
        str(get_settings().DATABASE_URI),
        maxPoolSize=get_settings().MAX_CONNECTIONS_COUNT,
        minPoolSize=get_settings().MIN_CONNECTIONS_COUNT,
    )
    print("Initialized Database.")


def close_mongo_connection():
    print("Closing Database...")
    if db.client:
        db.client.close()
    print("Database Closed")
