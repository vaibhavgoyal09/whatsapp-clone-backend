from dataclasses import dataclass
from typing import Generic, TypeVar, Union


T = TypeVar("T")


@dataclass
class Success(Generic[T]):
    data: T


@dataclass
class Error:
    code: int
    message: str = ""


ResultWrapper = Union[Success[T], Error]