"""Compatibility shim: re-export moved implementation from core.common.static_data.

This file preserves the original import path for existing callers and tests.
"""

from __future__ import annotations

from importlib import import_module

# Import the moved implementation and copy its attributes here, including
# underscore-prefixed helpers like `_load_json` which tests expect to exist
# on this module object.
_orig = import_module("src.core.common.static_data")
for _name in dir(_orig):
    if _name.startswith("__"):
        continue
    globals()[_name] = getattr(_orig, _name)

__all__ = [name for name in globals() if not name.startswith("__")]
