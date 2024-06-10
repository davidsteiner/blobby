from pathlib import Path

import pytest
from blobby.error import NoSuchKeyError
from storage_contexts import STORAGE_CONTEXTS, StorageContext


@pytest.mark.parametrize(["storage_context"], [(c,) for c in STORAGE_CONTEXTS])
def test_put_bytes(storage_context: StorageContext) -> None:
    with storage_context() as storage:
        data = b"hello world"

        relative_path = (Path("my_storage") / "test_file").as_posix()
        storage.put(key=relative_path, data=data)

        retrieved_data = storage.get(relative_path)

        assert data == retrieved_data


@pytest.mark.parametrize(["storage_context"], [(c,) for c in STORAGE_CONTEXTS])
def test_delete(storage_context: StorageContext) -> None:
    with storage_context() as storage:
        data = b"cats are cool"

        key = "animals/cat"
        storage.put(key=key, data=data)

        retrieved_data = storage.get(key)
        assert data == retrieved_data

        storage.delete(key)

        # The object should no longer exist and raise a NoSuchKeyError
        with pytest.raises(NoSuchKeyError):
            storage.get(key)

        # Subsequent calls to delete should also raise an exception
        with pytest.raises(NoSuchKeyError):
            storage.delete(key)
