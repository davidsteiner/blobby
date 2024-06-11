import typing

from blobby.storage import Storage, ObjectMeta

if typing.TYPE_CHECKING:
    from mypy_boto3_s3 import S3Client
else:
    S3Client = object


class S3Storage(Storage):
    def __init__(self, *, client: S3Client, bucket_name: str) -> None:
        self._client = client
        self._bucket_name = bucket_name

    def _put(self, key: str, data: bytes) -> None:
        self._client.put_object(Bucket=self._bucket_name, Key=key, Body=data)

    def get(self, key: str) -> bytes:
        try:
            output = self._client.get_object(Bucket=self._bucket_name, Key=key)
            return output["Body"].read()
        except self._client.exceptions.NoSuchKey:
            self.raise_key_not_found(key)

    def delete(self, key: str) -> None:
        try:
            # we only call head_object because delete_object does not raise
            # an exception when the object does not exist
            self._client.head_object(Bucket=self._bucket_name, Key=key)
            self._client.delete_object(Bucket=self._bucket_name, Key=key)
        except self._client.exceptions.ClientError as err:
            if err.response["Error"]["Code"] == "404":
                self.raise_key_not_found(key)
            else:
                raise

    def list(self, prefix: str) -> list[ObjectMeta]:
        response = self._client.list_objects_v2(Bucket=self._bucket_name, Prefix=prefix)

        return [ObjectMeta(key=meta["Key"]) for meta in response["Contents"]]
