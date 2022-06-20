from fastapi import APIRouter
from app.api.v1 import auth_routes, chat_routes, message_routes


api_v1_router = APIRouter(prefix='/api/v1', tags=["api_v1"])
api_v1_router.include_router(auth_routes.router)
api_v1_router.include_router(chat_routes.router)
api_v1_router.include_router(message_routes.router)