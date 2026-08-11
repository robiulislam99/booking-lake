"""
Qdrant connection + collection management + bulk upsert, following the
same client-wrapper pattern as dynamodb_client.py / es_client.py.
"""

from __future__ import annotations

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

from . import config as client_config

QDRANT_URL = client_config.QDRANT_URL
QDRANT_COLLECTION_NAME = client_config.QDRANT_COLLECTION_NAME
QDRANT_VECTOR_SIZE = client_config.QDRANT_VECTOR_SIZE
COLLECTION_NAME = QDRANT_COLLECTION_NAME
VECTOR_SIZE = QDRANT_VECTOR_SIZE


def get_qdrant_client() -> QdrantClient:
    return QdrantClient(url=client_config.os.environ.get("QDRANT_URL", client_config.QDRANT_URL))


def ensure_collection(client: QdrantClient):
    existing = [c.name for c in client.get_collections().collections]
    if client_config.QDRANT_COLLECTION_NAME in existing:
        return
    client.create_collection(
        collection_name=client_config.QDRANT_COLLECTION_NAME,
        vectors_config=VectorParams(size=client_config.QDRANT_VECTOR_SIZE, distance=Distance.COSINE),
    )


def bulk_upsert(points: list[PointStruct]):
    """points: list of qdrant_client.models.PointStruct, built by qdrant_document_mapper.py"""
    client = get_qdrant_client()
    ensure_collection(client)
    client.upsert(collection_name=QDRANT_COLLECTION_NAME, points=points)
