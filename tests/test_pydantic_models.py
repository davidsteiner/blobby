import pytest
from pydantic import BaseModel

from storage_contexts import STORAGE_CONTEXTS


class DummyData(BaseModel):
    str_field: str
    int_field: int


@pytest.mark.parametrize(["storage_context"], [(c,) for c in STORAGE_CONTEXTS])
def test_put_model_object(storage_context) -> None:
    with storage_context() as storage:
        data = DummyData(str_field="str_field", int_field=3)

        key = "animals/cat.json"
        storage.put_model_object(key=key, obj=data)

        retrieved_data = storage.get_model_object(key=key, object_type=DummyData)

        assert data == retrieved_data
