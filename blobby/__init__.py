from blobby.storage import Storage

from blobby.filesystem import FileSystemStorage
from blobby._gcp import GoogleCloudStorage
from blobby.memory import MemoryStorage

__all__ = [
    "FileSystemStorage",
    "MemoryStorage",
    "Storage",
]


try:
    import boto3  # noqa: F401
    from blobby._s3 import S3Storage  # noqa: F401

    __all__.append("S3Storage")
except ImportError:
    pass

try:
    from google.cloud import storage  # noqa: F401
    from blobby._gcp import GoogleCloudStorage  # noqa: F401

    __all__.append("GoogleCloudStorage")
except ImportError:
    pass
