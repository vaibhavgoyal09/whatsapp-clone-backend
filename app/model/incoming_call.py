from dataclasses import dataclass


@dataclass
class IncomingCall:
    call_type: str
    by_user_id: str
    to_user_id: str

    @staticmethod
    def from_dict(request_dict):
        return IncomingCall(
            call_type=request_dict["call_type"],
            by_user_id=request_dict["by_user_id"],
            to_user_id=request_dict["to_user_id"],
        )
