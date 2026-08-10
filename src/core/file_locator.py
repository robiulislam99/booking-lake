"""Compatibility shim: re-export moved implementation from core.ingestion.feed_reader.

Preserves the original public API so existing callers and tests continue
to import from `src.core.file_locator` as before.
"""

from __future__ import annotations

from src.core.ingestion.feed_reader import *  # noqa: F401,F403

__all__ = [name for name in globals() if not name.startswith("_")]
