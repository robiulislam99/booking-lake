"""Shared logging configuration helpers."""

import logging


def configure_logging(level: int = logging.INFO) -> None:
    logging.basicConfig(level=level)
