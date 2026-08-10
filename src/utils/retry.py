"""Simple retry helper for transient failures."""

from collections.abc import Callable
from functools import wraps
from time import sleep


def retry(*, attempts: int = 3, delay_seconds: float = 1.0, exceptions: tuple[type[Exception], ...] = (Exception,)):
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_error = None
            for attempt in range(attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as error:
                    last_error = error
                    if attempt + 1 < attempts:
                        sleep(delay_seconds)
            if last_error is not None:
                raise last_error

        return wrapper

    return decorator
