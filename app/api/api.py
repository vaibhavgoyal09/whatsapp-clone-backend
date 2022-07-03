from fastapi import APIRouter
from app.api.v1 import chat_routes, message_routes, file_upload_routes, user_routes


api_v1_router = APIRouter(prefix='/api/v1', tags=["api_v1"])
api_v1_router.include_router(user_routes.router)
api_v1_router.include_router(chat_routes.router)
api_v1_router.include_router(message_routes.router)
api_v1_router.include_router(file_upload_routes.router)