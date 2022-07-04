from fastapi import APIRouter, UploadFile, Depends, HTTPException
from app.file.file_service import FileService
from app.utils.result_wrapper import *
from fastapi.responses import ORJSONResponse


router = APIRouter(prefix="/file", tags=["file"])

@router.post("/new")
async def upload_image(file: UploadFile, service: FileService = Depends()):
    result: ResultWrapper = await service.upload_file(file)
    if isinstance(result, Error):
        raise HTTPException(status_code=result.code, detail=result.message)
    else:
        return ORJSONResponse(result)