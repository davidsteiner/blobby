import shutil
import tempfile
from pathlib import Path
from typing import Generator

import pytest


@pytest.fixture(scope="session")
def temp_dir() -> Generator[Path, None, None]:
    d = tempfile.mkdtemp()
    yield Path(d)
    shutil.rmtree(d)
