from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from fastapi.staticfiles import StaticFiles

from app.core.config import get_settings
from app.api.api import api_v1_router


def get_application():
    _app = FastAPI(title=get_settings().PROJECT_NAME, debug=True)

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin)
                       for origin in get_settings().BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    if not os.path.exists('static'):
        os.makedirs('static')

    _app.mount("/static", StaticFiles(directory="static"), name="static")

    return _app


app = get_application()
app.include_router(api_v1_router)


# For debugging use only

# from app.auth.firebase_service import get_current_user_uid

# def override_get_current_user_uid() -> str:
#     return "dnPBigVSLbUrZIkQrj0kWafjdJq2"


# app.dependency_overrides[get_current_user_uid] = override_get_current_user_uid


@app.get('/')
async def index_route():
    return {
        "message": "Hello, World!"
    }
