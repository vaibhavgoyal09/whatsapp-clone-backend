from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.api.v1.api import api_v1_router


def get_application():
    _app = FastAPI(title=get_settings().PROJECT_NAME, debug=True)

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in get_settings().BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return _app


app = get_application()
app.include_router(api_v1_router)


@app.get('/')
async def index_route():
    return {
        "message": "Hello, World!"
    }