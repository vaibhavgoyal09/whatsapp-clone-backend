from fastapi import APIRouter
from app.api.v1 import auth_routes, chat_routes


api_v1_router = APIRouter(prefix='/api/v1', tags=["api_v1"])
api_v1_router.include_router(auth.router)
api_v1_router.include_router(chat_routes.router)