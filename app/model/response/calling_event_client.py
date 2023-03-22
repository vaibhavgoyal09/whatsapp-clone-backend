from dataclasses import dataclass


@dataclass
class CallingEventClient:
    by_user_id: str
    event: int
