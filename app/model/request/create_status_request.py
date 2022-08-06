from dataclasses import dataclass


@dataclass
class CreateStatusRequest:
    type: int
    media_url: str
