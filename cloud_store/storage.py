from abc import ABC, abstractmethod
from typing import Type, TypeVar

from pydantic import BaseModel


T = TypeVar("T", bound=BaseModel)

_ENCODING = "utf-8"


class Storage(ABC):
    def put_model_object(self, *, key: str, obj: BaseModel) -> None:
        data = obj.json(by_alias=True)
        self.put(key=key, data=data.encode(_ENCODING))

    def get_model_object(self, *, key: str, object_type: Type[T]) -> T:
        data = self.get(key=key)
        return object_type.parse_raw(data)

    @staticmethod
    def encode(data: str) -> bytes:
        return data.encode(_ENCODING)

    @abstractmethod
    def put(self, key: str, data: bytes | str) -> None: ...

    @abstractmethod
    def get(self, key: str) -> bytes: ...

    @abstractmethod
    def delete(self, key: str) -> None: ...
