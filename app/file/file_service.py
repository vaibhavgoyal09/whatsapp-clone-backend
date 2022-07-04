import os
import uuid
from fastapi import UploadFile
from app.utils.result_wrapper import ResultWrapper, Error
import aiofiles
from app.utils import util
from app.model.response.file_upload_response import FileUploadResponse


class FileService:
    async def upload_file(self, file: UploadFile) -> ResultWrapper[FileUploadResponse]:
    
        file_extension = os.path.splitext(file.filename)[1]

        if not file_extension in util.ACCEPTABLE_FILE_FORMAT_EXTENSIONS:
            return Error(message='File format is not wrong acceptable')

        filename = f"{uuid.uuid4().hex}{file_extension}"
        content = await file.read()
        file_path = f"static/{filename}"

        async with aiofiles.open(f"{file_path}", mode="wb+") as f:
            await f.write(content)

        return FileUploadResponse(f"http://127.0.0.1:8000/static/{filename}")
