import functools
import time
from typing import Any, Callable, TypeVar, cast
from .logger import get_logger

F = TypeVar("F", bound=Callable[..., Any])
logger = get_logger(__name__)


def log_execution(func: F) -> F:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        started = time.perf_counter()
        try:
            result = func(*args, **kwargs)
            logger.info("%s completed in %.4fs", func.__name__, time.perf_counter() - started)
            return result
        except (OSError, ValueError, KeyError) as exc:
            logger.exception("%s failed: %s", func.__name__, exc)
            raise

    return cast(F, wrapper)
