import typing

from cloud_store.storage import Storage

if typing.TYPE_CHECKING:
    from mypy_boto3_s3 import S3Client


class S3Storage(Storage):
    def __init__(self, client: S3Client, bucket_name: str) -> None:
        self._client = client
        self._bucket_name = bucket_name

    def put(self, key: str, data: bytes | str) -> None:
        return None

    def get(self, key: str) -> bytes:
        return b""

    def delete(self, key: str) -> None:
        return None
