from typing import Dict
from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.online_users: Dict[str, WebSocket] = dict()

    def add_user(self, user_id: str, websocket: WebSocket):
        self.online_users[user_id] = websocket

    def remove_user(self, user_id: str):
        self.online_users.pop(user_id)

    def get_websocket_for_user(self, user_id: str) -> WebSocket:
        return self.online_users.get(user_id)


manager = ConnectionManager()