from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi import Depends
from data.database import get_database, CollectionNames
from app.model.request.create_status_request import CreateStatusRequest
from datetime import datetime
from domain.model.status import Status
from typing import List


class StatusRepository:
    def __init__(self, database: AsyncIOMotorDatabase = Depends(get_database)) -> None:
        self.status_collection = database[CollectionNames.STATUS_COLLECTION]

    async def add_status(self, user_self_id: str, request: CreateStatusRequest) -> str:
        status = {
            "type": request.type,
            "media_url": request.media_url,
            "user_id": user_self_id,
            "created_at": int(datetime.timestamp(datetime.now()) * 1000),
        }
        result = await self.status_collection.insert_one(status)

        return str(result.inserted_id)
 
    async def get_all_statuses_of_user(self, user_id: str) -> List[Status]:
        cursor = self.status_collection.find_one({"user_id": user_id}).sort("created_at")
        statuses: List[Status] = list()

        async for document in cursor:
            statuses.append(Status.from_db_model(document))

        statuses.reverse()
        return statuses
