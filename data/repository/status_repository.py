from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi import Depends
from data.database import get_database, CollectionNames
from app.model.request.create_status_request import CreateStatusRequest
from datetime import datetime
from domain.model.status import Status
from typing import List


class StatusRepository:
    def __init__(self, database: AsyncIOMotorDatabase = Depends(get_database)) -> None:
        self.status_collection = database[CollectionNames.STATUS_COLLECTION.value]

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
        last_24_hours_start_timestamp = int(
            datetime.timestamp(datetime.now()) * 1000 - (24 * 60 * 60 * 1000)
        )
        cursor = self.status_collection.find(
            {
                "$and": [
                    {"user_id": user_id},
                    {"created_at": {"$gte": last_24_hours_start_timestamp}},
                ]
            }
        ).sort("created_at")
        statuses: List[Status] = list()

        async for document in cursor:
            statuses.append(Status.from_db_model(document))

        statuses.reverse()
        return statuses

    async def get_all_user_ids_with_active_status(self) -> List[str]:
        last_24_hours_start_timestamp = int(
            datetime.timestamp(datetime.now()) * 1000 - (24 * 60 * 60 * 1000)
        )
        cursor = self.status_collection.find(
            {"created_at": {"$gte": last_24_hours_start_timestamp}}
        ).sort("created_at")

        user_ids: List[str] = list()

        async for document in cursor:
            user_id = document.get("user_id")
            if not user_id:
                continue
            user_ids.append(user_id)

        user_ids.reverse()
        return user_ids
