from dataclasses import dataclass
from typing import Generic, TypeVar, Union


T = TypeVar("T")


@dataclass
class Error:
    code: int = 400
    message: str = ""


ResultWrapper = Union[T, Error]
