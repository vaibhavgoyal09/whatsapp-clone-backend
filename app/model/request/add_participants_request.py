from dataclasses import dataclass


@dataclass
class AddParticipantsRequest:
    group_id: str
    user_ids: list[str]
