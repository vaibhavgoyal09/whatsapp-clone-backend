from dataclasses import dataclass


@dataclass
class IncomingCallResponseClient:
    by_user_id: str
    response: int
