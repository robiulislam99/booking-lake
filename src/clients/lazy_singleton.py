"""
Generic lazy-singleton helper -- construct something expensive exactly
once per process, reuse it after. Currently only embedding_client.py
does this (for the sentence-transformers model); es_client.py,
qdrant_client.py, and dynamodb_client.py currently rebuild their
client/resource on every call instead. Use this to make that
consistent, if/when that inconsistency is worth fixing.
"""

from collections.abc import Callable
from typing import TypeVar

T = TypeVar("T")


def lazy_singleton(factory: Callable[[], T]) -> Callable[[], T]:
    """
    Wraps a zero-arg factory function so it only actually runs once.
    Usage:
        _get_model = lazy_singleton(lambda: SentenceTransformer(MODEL_NAME))
    """
    cache = {}

    def get() -> T:
        if "value" not in cache:
            cache["value"] = factory()
        return cache["value"]

    return get
