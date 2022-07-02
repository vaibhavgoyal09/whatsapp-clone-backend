from fastapi import APIRouter, UploadFile
import os
import uuid

router = APIRouter(prefix="/file", tags=["file_upload"])

@router.post("/new")
async def upload_image(file: UploadFile):
    print(file.filename)
    file_extension = os.path.splitext(file.filename)[1]
    filename = f"{uuid.uuid4().hex}{file_extension}"
    content = await file.read()
    file_path = f"static/{filename}"
    file_input = open(f'{file_path}', 'wb+')
    file_input.write(content)  

    return {
        "url": f"http://127.0.0.1:8000/static/{filename}"
    }
