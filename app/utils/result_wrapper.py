from dataclasses import dataclass
from typing import Generic, TypeVar, Union


T = TypeVar("T")


@dataclass
class Error:
    code: int = 400
    message: str = "Something Went Wrong"


ResultWrapper = Union[T, Error]
