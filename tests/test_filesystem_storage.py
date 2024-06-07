from pathlib import Path

from pydantic import BaseModel

from cloud_store import FileSystemStorage


def test_put_bytes(temp_dir) -> None:
    data = b"hello world"
    storage = FileSystemStorage(temp_dir, create_missing_dirs=True)

    relative_path = Path("my_storage") / "test_file"
    storage.put(path=relative_path, data=data)

    retrieved_data = storage.get(relative_path)

    assert data == retrieved_data


class TestData(BaseModel):
    str_field: str
    int_field: int


def test_put_model_object(temp_dir) -> None:
    data = TestData(str_field="str_field", int_field=3)
    storage = FileSystemStorage(temp_dir, create_missing_dirs=True)

    relative_path = Path("my_storage") / "test_model_file"
    storage.put_model_object(path=relative_path, obj=data)

    retrieved_data = storage.get_model_object(path=relative_path, object_type=TestData)

    assert data == retrieved_data
