from typing import Optional, Protocol


class CachePort(Protocol):
    """Port for caching operations."""

    def get(self, key: str) -> Optional[str]: ...

    def set(self, key: str, value: str, ttl: Optional[int] = None) -> None: ...

    def delete(self, key: str) -> None: ...
