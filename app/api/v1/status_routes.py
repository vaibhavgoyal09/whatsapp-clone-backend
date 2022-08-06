from fastapi import Depends, HTTPException, APIRouter
from fastapi.responses import ORJSONResponse
from app.model.request.create_status_request import CreateStatusRequest
from app.service.firebase_service import get_current_user
from domain.model.user import User
from app.service.status_service import StatusService
from app.utils.result_wrapper import ResultWrapper, Error


router = APIRouter(prefix="/status", tags=["status"])


@router.post("/new")
async def create_new_status(
    request: CreateStatusRequest,
    user: User = Depends(get_current_user),
    service: StatusService = Depends(),
):
    result: ResultWrapper = await service.add_status(user.id, request)
    if isinstance(result, Error):
        raise HTTPException(status_code=result.code, detail=result.message)
    else:
        return ORJSONResponse(result)
