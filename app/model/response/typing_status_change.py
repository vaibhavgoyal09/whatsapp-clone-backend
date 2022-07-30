from dataclasses import dataclass


@dataclass
class TypingStatusChange:
    user_id: str
    chat_id: str
    is_typing: bool
