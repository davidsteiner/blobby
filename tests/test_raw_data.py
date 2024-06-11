import pytest

from blobby.error import NoSuchKeyError
from storage_contexts import STORAGE_CONTEXTS, StorageContext


@pytest.mark.parametrize(["storage_context"], [(c,) for c in STORAGE_CONTEXTS])
def test_put_bytes(storage_context: StorageContext) -> None:
    with storage_context() as storage:
        data = b"hello world"

        key = "my-storage/foo"
        storage.put(key=key, data=data)

        retrieved_data = storage.get(key)

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


@pytest.mark.parametrize(["storage_context"], [(c,) for c in STORAGE_CONTEXTS])
def test_list(storage_context: StorageContext) -> None:
    with storage_context() as storage:
        storage.put("1/foo/file.txt", "test-data")
        storage.put("1/fool.txt", "test-data")
        storage.put("2/foo/file.txt", "test-data")
        storage.put("1/bar/file.txt", "test-data")
        storage.put("1/fo/file.txt", "test-data")

        objects = storage.list("1/foo")
        keys = [o.key for o in objects]

        assert set(keys) == {"1/foo/file.txt", "1/fool.txt"}
