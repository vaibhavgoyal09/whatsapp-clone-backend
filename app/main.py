import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.api import api_v1_router, ws_router
from app.core.config import get_settings
from data.database import connect_to_mongo, close_mongo_connection


def get_application():
    _app = FastAPI(title=get_settings().PROJECT_NAME, debug=True)

    _app.add_event_handler("startup", connect_to_mongo)
    _app.add_event_handler("shutdown", close_mongo_connection)
    
    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in get_settings().BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    if not os.path.exists("static"):
        os.makedirs("static")
    _app.mount("/static", StaticFiles(directory="static"), name="static")
    return _app


app = get_application()
app.include_router(api_v1_router)
app.include_router(ws_router)


@app.get("/")
async def index_route():
    return {"message": "Hello, World!"}
