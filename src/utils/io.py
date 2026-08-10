"""Small filesystem read/write helpers intended for external use.

Keep simple, well-typed helpers here so other packages (clients,
scripts, tests) can perform common file I/O without duplicating code.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def ensure_dir(path: str | Path) -> Path:
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


def read_text(path: str | Path) -> str:
    # Accept either a path-like or an object that implements .read_text()
    if hasattr(path, "read_text"):
        return path.read_text()
    return Path(path).read_text(encoding="utf-8")


def write_text(path: str | Path, data: str) -> None:
    # Accept either a path-like or an object that implements .write_text()
    if hasattr(path, "write_text"):
        return path.write_text(data)
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(data, encoding="utf-8")


def read_bytes(path: str | Path) -> bytes:
    if hasattr(path, "read_bytes"):
        return path.read_bytes()
    return Path(path).read_bytes()


def write_bytes(path: str | Path, data: bytes) -> None:
    if hasattr(path, "write_bytes"):
        return path.write_bytes(data)
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(data)


def read_json(path: str | Path) -> Any:
    return json.loads(read_text(path))


def write_json(path: str | Path, obj: Any) -> None:
    write_text(path, json.dumps(obj, ensure_ascii=False, indent=2))


def list_files(path: str | Path, pattern: str = "**/*") -> list[Path]:
    p = Path(path)
    if not p.exists():
        return []
    return [x for x in p.glob(pattern) if x.is_file()]
