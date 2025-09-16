from typing import Optional

from src.domain.ports.cache_port import CachePort


class MockCache(CachePort):
    """In-memory mock cache for testing."""

    def __init__(self):
        self._cache: dict[str, str] = {}

    def get(self, key: str) -> Optional[str]:
        """Retrieve value from cache by key."""
        return self._cache.get(key)

    def set(self, key: str, value: str, ttl: Optional[int] = None) -> None:
        """Store value in cache with optional TTL in seconds."""
        self._cache[key] = value

    def delete(self, key: str) -> None:
        """Delete value from cache by key."""
        self._cache.pop(key, None)

    def clear(self) -> None:
        """Clear all cached values."""
        self._cache.clear()
