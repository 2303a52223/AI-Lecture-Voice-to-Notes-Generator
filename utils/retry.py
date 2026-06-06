"""
Retry utilities for transient operations (model loads, network calls).
Provides a simple `retry_call` function and `retry` decorator with exponential backoff.
"""
import time
from typing import Callable, Type, Tuple


def retry_call(fn: Callable, exceptions: Tuple[Type[BaseException], ...] = (Exception,), tries: int = 3, delay: float = 1.0, backoff: float = 2.0):
    """
    Call `fn()` and retry on specified exceptions.

    Args:
        fn: Callable with no args to execute.
        exceptions: Exceptions to catch and retry on.
        tries: Number of attempts (including first).
        delay: Initial delay in seconds before retrying.
        backoff: Multiplier applied to delay after each failure.

    Returns:
        The result of `fn()` if successful.

    Raises:
        The last exception raised by `fn()` if all retries fail.
    """
    attempt = 0
    current_delay = delay
    last_exc = None
    while attempt < tries:
        try:
            return fn()
        except exceptions as e:
            last_exc = e
            attempt += 1
            if attempt >= tries:
                break
            time.sleep(current_delay)
            current_delay *= backoff
    # re-raise last exception
    raise last_exc


def retry(exceptions: Tuple[Type[BaseException], ...] = (Exception,), tries: int = 3, delay: float = 1.0, backoff: float = 2.0):
    """Decorator version of retry_call for functions that accept arbitrary args/kwargs."""
    def decorator(fn: Callable):
        def wrapped(*args, **kwargs):
            return retry_call(lambda: fn(*args, **kwargs), exceptions=exceptions, tries=tries, delay=delay, backoff=backoff)
        return wrapped
    return decorator
