from pathlib import Path

from cloud_store.storage import Storage


class FileSystemStorage(Storage):

    def __init__(self, root_dir: Path, *, create_missing_dirs: bool = False) -> None:
        self._root_dir = root_dir
        self._create_missing_dirs = create_missing_dirs

    def put(self, path: Path, data: bytes | str) -> None:
        if isinstance(data, str):
            data = self.encode(data)

        full_path = self._full_path(path)
        if self._create_missing_dirs:
            full_path.parent.mkdir(parents=True, exist_ok=True)

        full_path.write_bytes(data)

    def get(self, path: Path) -> bytes:
        return self._full_path(path).read_bytes()

    def delete(self, path: Path) -> None:
        self._full_path(path).unlink()

    def _full_path(self, path: Path) -> Path:
        return self._root_dir / path
