from typing import Dict
from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.online_users: Dict[int, WebSocket] = dict()

    def add_user(self, user_id: int, websocket: WebSocket):
        self.online_users[user_id] = websocket

    def remove_user(self, user_id: int):
        self.online_users.pop(user_id)

    def get_websocket_for_user(self, user_id: int) -> WebSocket:
        return self.online_users[user_id]


manager = ConnectionManager()