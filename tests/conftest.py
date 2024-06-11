from typing import Iterator

import pytest
from gcp_storage_emulator.server import create_server
from moto import mock_aws


@pytest.fixture(scope="session", autouse=True)
def mock_s3() -> Iterator[None]:
    mock = mock_aws()
    mock.start()

    yield

    mock.stop()


@pytest.fixture(scope="session", autouse=True)
def mock_google_cloud_storage() -> Iterator[None]:
    with pytest.MonkeyPatch.context() as patch:
        host = "localhost"
        port = 9023
        server = create_server(
            host=host, port=port, in_memory=True, default_bucket="blobby-test"
        )

        patch.setenv("STORAGE_EMULATOR_HOST", f"http://{host}:{port}")

        server.start()
        yield
        server.stop()
