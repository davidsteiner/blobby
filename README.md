<div align="center">

# Blobby

**A cloud agnostic object storage library.**

[![PyPI Versions Badge](https://badge.fury.io/py/blobby.svg)](https://badge.fury.io/py/blobby/)
[![PyPI Versions Badge](https://img.shields.io/pypi/pyversions/blobby.svg)](https://pypi.org/project/blobby/)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/5c800180fb3b466fb8964d798aecdcc2)](https://app.codacy.com/gh/davidsteiner/blobby/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)
[![Codacy Badge](https://app.codacy.com/project/badge/Coverage/5c800180fb3b466fb8964d798aecdcc2)](https://app.codacy.com/gh/davidsteiner/blobby/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_coverage)

</div>

---

Blobby provides uniform interface for object storage solutions of common cloud providers.
It also provides a local filesystem-based implementation and an in-memory implementation
for local development and testing.

In addition to the core APIs for manipulating and retrieving
binary data, blobby also provides convenient wrappers to 
write and read
[pydantic](https://docs.pydantic.dev/latest/) objects
serialised as JSON documents.

## Provider support

- [x] AWS S3
- [x] Google Cloud Storage
- [x] Filesystem
- [x] In-memory
- [ ] Azure Blob Storage

## Creating a storage

All storage implementations inherit from `blobby.Storage` and
offer a uniform API.

### AWS S3 storage

> :warning: **Install blobby with the `aws` extra, i.e.**
> `pip install blobby[aws]`

The S3 implementation uses a `boto3` client, which needs to be
passed in when the storage is initialised. An S3 storage object
represents a bucket, whose name also needs to be supplied.

```python
import boto3
from blobby.aws import S3Storage

client = boto3.client("s3")
storage = S3Storage(client=client, bucket_name="my-bucket")
```

### Azure Blob Storage

> :warning: **Install blobby with the `azure` extra, i.e.**
> `pip install blobby[azure]`

The Azure implementation leverages the Azure SDK for Python.
The storage expects the storage client to be provided.

```python
from azure.storage.blob import BlobServiceClient
from blobby.azure import AzureBlobStorage

url = "<connection_string>"
service_client = BlobServiceClient.from_connection_string(url)
container_client = service_client.create_container("my-container")

storage = AzureBlobStorage(container_client)
```

### Google Cloud Storage

> :warning: **Install blobby with the `gcp` extra, i.e.**
> `pip install blobby[gcp]`

The Google Cloud Storage leverages the official SDK for 
Cloud Storage. The bucket object needs to be supplied to the
storage when it's initialised.

```python
from google.cloud.storage import Client
from blobby.gcp import GoogleCloudStorage

client = Client()
bucket = client.bucket("my-bucket")
storage = GoogleCloudStorage(bucket)
```

### Filesystem storage

When creating a filesystem-based storage, the root directory
needs to be provided. All files will be relative to this 
directory.

```python
from blobby.filesystem import FileSystemStorage

storage = FileSystemStorage(root_dir="/my/storage/", create_missing_dirs=True)
```

The `create_missing_dirs` flag controls whether the root directory
will be automatically created if it doesn't already exist.

### In-memory storage

The in-memory implementation is backed with a simple dictionary stored
in memory.

```python
from blobby.memory import MemoryStorage

storage = MemoryStorage()
```

## Common operations

### Putting objects

The `put` operation works with `bytes` and `str` inputs.
In either case, the object is stored as a binary blob.

```python
key = "my-object"
data = b"hello world"
storage.put(key, data)
```

In the case of filesystem storage, the key needs to be a 
valid path.

### Getting objects

```python
key = "my-object"
storage.get(key)
```

### Deleting objects

```python
key = "my-object"
storage.delete(key)
```

### Listing objects

Currently, only listing by object prefix is supported.
This isn't very natural for filesystems, but the primary focus
of this library is object storage solutions, which often
don't have the concept of a folder or directory.

```python
prefix = "my/prefix"
storage.list(prefix)
```

## Pydantic objects

Pydantic objects can be written and read using 
dedicated APIs for convenience.

```python
class MyData(pydantic.BaseModel):
    foo: str
    bar: int

key = "my/data"
data = MyData(foo="hello", bar=1)

storage.put_model_object(key, data)
```

## Error handling

Storage implementations map their internal errors
to shared error types, which are contained in `blobby.error`.

```python
from blobby.error import NoSuchKeyError

try:
    storage.get("test")
except NoSuchKeyError as err:
    # do something with err
    pass
```