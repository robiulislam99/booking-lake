"""
Generic lazy-singleton helper -- construct something expensive exactly
once per process, reuse it after.
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
