"""Central client registry for convenience imports inside `src/clients`.

Other modules in `src/clients` can import this module to access the
concrete client implementations with stable names, e.g. ``client.s3_local``.
This keeps client construction in one place and simplifies internal imports.
"""

from __future__ import annotations

from . import (
    dynamodb_client,
    embedding_client,
    es_client,
    qdrant_client,
    s3_local_client,
    spark_session,
    sqs_client,
)

# Public aliases for convenience
dynamodb = dynamodb_client
es = es_client
embedding = embedding_client
qdrant = qdrant_client
s3_local = s3_local_client
spark = spark_session
sqs = sqs_client

__all__ = ["dynamodb", "es", "embedding", "qdrant", "s3_local", "spark", "sqs"]
