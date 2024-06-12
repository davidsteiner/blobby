import shutil
import tempfile
import uuid
from contextlib import contextmanager, AbstractContextManager
from pathlib import Path
from typing import Iterator, Callable

import boto3
from azure.storage.blob import BlobServiceClient
from google.cloud.storage import Client as GoogleClient

from blobby import (
    FileSystemStorage,
    GoogleCloudStorage,
    S3Storage,
    Storage,
    MemoryStorage,
)
from blobby.azure import AzureBlobStorage

StorageContext = Callable[[], AbstractContextManager[Storage]]


@contextmanager
def filesystem_storage() -> Iterator[Storage]:
    d = tempfile.mkdtemp()
    root_dir = Path(d)

    yield FileSystemStorage(root_dir=root_dir, create_missing_dirs=True)

    shutil.rmtree(d)


@contextmanager
def memory_storage() -> Iterator[Storage]:
    yield MemoryStorage()


@contextmanager
def s3_storage() -> Iterator[Storage]:
    bucket_name = uuid.uuid4().hex
    client = boto3.client("s3")
    client.create_bucket(
        Bucket=bucket_name,
        CreateBucketConfiguration={"LocationConstraint": "eu-west-1"},
    )

    yield S3Storage(client=client, bucket_name=bucket_name)


@contextmanager
def gcp_storage() -> Iterator[Storage]:
    client = GoogleClient()
    bucket = client.bucket("blobby-test")

    yield GoogleCloudStorage(bucket)


@contextmanager
def azure_blob_storage() -> Iterator[Storage]:
    url = "DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;"
    service_client = BlobServiceClient.from_connection_string(url)
    container_client = service_client.create_container(uuid.uuid4().hex)

    yield AzureBlobStorage(container_client)


STORAGE_CONTEXTS = [
    azure_blob_storage,
    filesystem_storage,
    gcp_storage,
    memory_storage,
    s3_storage,
]
