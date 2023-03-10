from dataclasses import dataclass


@dataclass
class IncomingCallResponse:
    by_user_id: str
    to_user_id: str
    response: int

    @staticmethod
    def from_dict(r_dict):
        return IncomingCallResponse(
            r_dict["by_user_id"], r_dict["to_user_id"], r_dict["respone"]
        )
