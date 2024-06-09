from cloud_store import Storage


class MemoryStorage(Storage):
    def __init__(self) -> None:
        self._storage: dict[str, bytes] = {}

    def _put(self, key: str, data: bytes) -> None:
        self._storage[key] = data

    def get(self, key: str) -> bytes:
        try:
            return self._storage[key]
        except KeyError:
            self.raise_key_not_found(key)

    def delete(self, key: str) -> None:
        try:
            del self._storage[key]
        except KeyError:
            self.raise_key_not_found(key)
