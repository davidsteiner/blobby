from pathlib import Path

from cloud_store.storage import Storage


class FileSystemStorage(Storage):
    def __init__(self, root_dir: Path, *, create_missing_dirs: bool = False) -> None:
        self._root_dir = root_dir
        self._create_missing_dirs = create_missing_dirs

    def put(self, key: str, data: bytes | str) -> None:
        if isinstance(data, str):
            data = self.encode(data)

        full_path = self._full_path(key)
        if self._create_missing_dirs:
            full_path.parent.mkdir(parents=True, exist_ok=True)

        full_path.write_bytes(data)

    def get(self, key: str) -> bytes:
        return self._full_path(key).read_bytes()

    def delete(self, key: str) -> None:
        self._full_path(key).unlink()

    def _full_path(self, key: Path | str) -> Path:
        return self._root_dir / key
