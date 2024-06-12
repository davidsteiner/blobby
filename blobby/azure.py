from azure.core.exceptions import ResourceNotFoundError
from azure.storage.blob import ContainerClient

from blobby import Storage
from blobby.storage import ObjectMeta


class AzureBlobStorage(Storage):
    def __init__(self, client: ContainerClient):
        self._client = client

    def _put(self, key: str, data: bytes) -> None:
        self._client.upload_blob(key, data)

    def get(self, key: str) -> bytes:
        try:
            return self._client.download_blob(key).read()
        except ResourceNotFoundError:
            self.raise_key_not_found(key)

    def delete(self, key: str) -> None:
        try:
            self._client.delete_blob(key)
        except ResourceNotFoundError:
            self.raise_key_not_found(key)

    def list(self, prefix: str) -> list[ObjectMeta]:
        blobs = self._client.list_blobs(name_starts_with=prefix)

        return [ObjectMeta(key=b.name) for b in blobs]
