from typing import Iterator

import pytest
from moto import mock_aws


@pytest.fixture(scope="session", autouse=True)
def mock_s3() -> Iterator[None]:
    mock = mock_aws()
    mock.start()

    yield

    mock.stop()
