from google.cloud.exceptions import NotFound
from google.cloud.storage import Bucket

from blobby import Storage
from blobby.storage import ObjectMeta


class GoogleCloudStorage(Storage):
    def __init__(self, bucket: Bucket) -> None:
        self._bucket = bucket

    def _put(self, key: str, data: bytes) -> None:
        self._bucket.blob(key).upload_from_string(
            data, content_type="application/octet-stream"
        )

    def get(self, key: str) -> bytes:
        try:
            return self._bucket.blob(key).download_as_bytes()
        except NotFound:
            self.raise_key_not_found(key)

    def delete(self, key: str) -> None:
        try:
            self._bucket.blob(key).delete()
        except NotFound:
            self.raise_key_not_found(key)

    def list(self, prefix: str) -> list[ObjectMeta]:
        blobs = self._bucket.list_blobs(prefix=prefix)

        return [ObjectMeta(key=b.name) for b in blobs]
