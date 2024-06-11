from abc import ABC, abstractmethod
from typing import Type, TypeVar, NoReturn

from pydantic import BaseModel

from blobby.error import NoSuchKeyError

T = TypeVar("T", bound=BaseModel)

_ENCODING = "utf-8"


class ObjectMeta(BaseModel):
    key: str


class Storage(ABC):
    def put_model_object(self, *, key: str, obj: BaseModel) -> None:
        data = obj.model_dump_json(by_alias=True)
        self.put(key=key, data=data.encode(_ENCODING))

    def get_model_object(self, *, key: str, object_type: Type[T]) -> T:
        data = self.get(key=key)
        return object_type.model_validate_json(data)

    @staticmethod
    def _encode(data: str) -> bytes:
        return data.encode(_ENCODING)

    def put(self, key: str, data: bytes | str) -> None:
        if isinstance(data, str):
            data = self._encode(data)

        return self._put(key, data)

    @abstractmethod
    def _put(self, key: str, data: bytes) -> None: ...

    @abstractmethod
    def get(self, key: str) -> bytes: ...

    @abstractmethod
    def delete(self, key: str) -> None: ...

    @abstractmethod
    def list(self, prefix: str) -> list[ObjectMeta]: ...

    def raise_key_not_found(self, key: str) -> NoReturn:
        raise NoSuchKeyError(f"key {key} not found")
