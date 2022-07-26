from fastapi import APIRouter
from app.api.v1 import chat_routes, file_routes, message_routes, user_routes, group_routes
from app.api.ws import chat_ws_routes

api_v1_router = APIRouter(prefix="/api/v1", tags=["api_v1"])
api_v1_router.include_router(user_routes.router)
api_v1_router.include_router(chat_routes.router)
api_v1_router.include_router(message_routes.router)
api_v1_router.include_router(file_routes.router)
api_v1_router.include_router(group_routes.router)

ws_router = APIRouter(prefix="/ws", tags=["ws"])
ws_router.include_router(chat_ws_routes.router)
