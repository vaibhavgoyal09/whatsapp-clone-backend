from dataclasses import dataclass


@dataclass
class RemoveParticipantsRequest:
    group_id: str
    user_ids: list[str]
