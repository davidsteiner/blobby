from pathlib import Path

from blobby.storage import Storage, ObjectMeta


class FileSystemStorage(Storage):
    def __init__(self, root_dir: Path, *, create_missing_dirs: bool = False) -> None:
        self._root_dir = root_dir
        self._create_missing_dirs = create_missing_dirs

    def _put(self, key: str, data: bytes) -> None:
        full_path = self._full_path(key)
        if self._create_missing_dirs:
            full_path.parent.mkdir(parents=True, exist_ok=True)

        full_path.write_bytes(data)

    def get(self, key: str) -> bytes:
        try:
            return self._full_path(key).read_bytes()
        except FileNotFoundError:
            self.raise_key_not_found(key)

    def delete(self, key: str) -> None:
        try:
            self._full_path(key).unlink()
        except FileNotFoundError:
            self.raise_key_not_found(key)

    def list(self, prefix: str) -> list[ObjectMeta]:
        paths: list[Path] = []

        for path in self._root_dir.rglob(f"{prefix}*"):
            if path.is_dir():
                paths.extend(p for p in path.rglob("*") if p.is_file())
            else:
                paths.append(path)

        relative_paths = (p.relative_to(self._root_dir).as_posix() for p in paths)
        return [ObjectMeta(key=p) for p in relative_paths]

    def _full_path(self, key: Path | str) -> Path:
        return self._root_dir / key
