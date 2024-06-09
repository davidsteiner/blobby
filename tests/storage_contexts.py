import shutil
import tempfile
import uuid
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

import boto3

from cloud_store import FileSystemStorage, S3Storage, Storage


@contextmanager
def filesystem_storage() -> Iterator[Storage]:
    d = tempfile.mkdtemp()
    root_dir = Path(d)

    yield FileSystemStorage(root_dir=root_dir, create_missing_dirs=True)

    shutil.rmtree(d)


@contextmanager
def s3_storage() -> Iterator[Storage]:
    bucket_name = uuid.uuid4().hex
    client = boto3.client("s3")
    client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={"LocationConstraint": "eu-west-1"})

    yield S3Storage(client=client, bucket_name=bucket_name)


STORAGE_CONTEXTS = [filesystem_storage, s3_storage]
