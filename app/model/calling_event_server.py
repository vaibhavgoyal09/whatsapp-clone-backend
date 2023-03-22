from dataclasses import dataclass
from enum import Enum


class CallingEventType(Enum):
    aborted = (0,)
    disconnected = 1


@dataclass
class CallingEventServer:
    to_user_id: str
    event: int

    @staticmethod
    def from_dict(r_dict):
        return CallingEventServer(
            to_user_id=r_dict["to_user_id"], event=r_dict["event"]
        )
