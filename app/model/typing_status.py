from dataclasses import dataclass


@dataclass
class TypingStatus:
    is_typing: bool
    chat_id: str

    @staticmethod
    def from_dict(dict):
        return TypingStatus(
            is_typing=dict.get("is_typing"),
            chat_id=dict.get("chat_id")
            )
