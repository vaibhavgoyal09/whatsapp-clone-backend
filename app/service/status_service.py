from typing import List
from fastapi import Depends
from app.utils.result_wrapper import Error, ResultWrapper
from data.repository.status_repository import StatusRepository
from app.model.request.create_status_request import CreateStatusRequest
import traceback

from domain.model.status import Status


class StatusService:
    def __init__(self, status_repository: StatusRepository = Depends()) -> None:
        self.status_repository = status_repository

    async def add_status(
        self, user_self_id: str, request: CreateStatusRequest
    ) -> ResultWrapper[str]:
        try:
            return await self.status_repository.add_status(user_self_id, request)
        except:
            traceback.print_exc()
            return Error()

    async def get_all_statuses_of_user(
        self, user_id: str
    ) -> ResultWrapper[List[Status]]:
        try:
            return await self.status_repository.get_all_statuses_of_user(user_id)
        except:
            traceback.print_exc()
            return Error()
