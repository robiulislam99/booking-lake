"""Small helpers for reading environment-driven configuration."""

import os


def get_env(name: str, default: str | None = None) -> str | None:
    return os.environ.get(name, default)


def get_required_env(name: str) -> str:
    value = os.environ.get(name)
    if value is None or value == "":
        raise KeyError(f"Missing required environment variable: {name}")
    return value
