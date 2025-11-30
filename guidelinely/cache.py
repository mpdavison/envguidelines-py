"""Client-side caching for Guidelinely API calculation endpoints.

Uses diskcache for persistent, SQLite-backed caching that survives between runs.

The cache directory can be configured via the GUIDELINELY_CACHE_DIR environment
variable. If not set, defaults to ~/.guidelinely_cache.
"""

import os
from pathlib import Path
from typing import Any, Optional, cast

from diskcache import Cache  # type: ignore[import-untyped]

__all__ = ["get_cached", "set_cached", "cache", "CACHE_DIR"]

# Cache directory: configurable via environment variable, defaults to user's home directory
_default_cache_dir = Path.home() / ".guidelinely_cache"
CACHE_DIR = Path(os.getenv("GUIDELINELY_CACHE_DIR", str(_default_cache_dir)))
cache = Cache(directory=str(CACHE_DIR))


def get_cached(key_data: dict[str, Any]) -> Optional[dict[str, Any]]:
    """Retrieve cached response for given request data.

    Args:
        key_data: Cache key (typically dict of request parameters)

    Returns:
        Cached response data if found, None otherwise
    """
    result = cache.get(key_data)
    if result is None:
        return None
    return cast(dict[str, Any], result)


def set_cached(key_data: dict[str, Any], value: dict[str, Any], ttl: int = 24 * 3600) -> None:
    """Store response in cache for given request data with TTL.

    Args:
        key_data: Cache key (typically dict of request parameters)
        value: Response data to cache
        ttl: Time to live in seconds (default: 24 hours)
    """
    cache.set(key_data, value, expire=ttl)
