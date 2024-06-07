from abc import ABC, abstractmethod
from pathlib import Path
from typing import Type, TypeVar

from pydantic import BaseModel


T = TypeVar("T", bound=BaseModel)

_ENCODING = "utf-8"


class Storage(ABC):
    def put_model_object(self, *, path: Path, obj: BaseModel) -> None:
        data = obj.json(by_alias=True)
        self.put(path=path, data=data.encode(_ENCODING))

    def get_model_object(self, *, path: Path, object_type: Type[T]) -> T:
        data = self.get(path=path)
        return object_type.parse_raw(data)

    @staticmethod
    def encode(data: str) -> bytes:
        return data.encode(_ENCODING)

    @abstractmethod
    def put(self, path: Path, data: bytes | str) -> None: ...

    @abstractmethod
    def get(self, path: Path) -> bytes: ...

    @abstractmethod
    def delete(self, path: Path) -> bytes: ...
