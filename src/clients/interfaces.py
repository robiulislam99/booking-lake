"""Abstract client contracts used by the thin adapters."""

from collections.abc import Sequence
from typing import Any, Protocol


class DocumentStoreClient(Protocol):
    def bulk_upsert(self, items: Sequence[dict[str, Any]]) -> None:
        """Write or replace a batch of documents."""
