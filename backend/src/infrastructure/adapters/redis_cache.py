from typing import Optional

import redis


class RedisCache:
    """Redis implementation of CachePort."""

    def __init__(self, redis_client: redis.Redis):
        self._redis = redis_client

    def get(self, key: str) -> Optional[str]:
        try:
            cached_data = self._redis.get(key)
            return cached_data.decode("utf-8") if cached_data else None
        except redis.RedisError:
            return None

    def set(self, key: str, value: str, ttl: Optional[int] = None) -> None:
        try:
            if ttl:
                self._redis.setex(key, ttl, value)
            else:
                self._redis.set(key, value)
        except redis.RedisError:
            pass

    def delete(self, key: str) -> None:
        """Delete value from cache by key."""
        try:
            self._redis.delete(key)
        except redis.RedisError:
            pass
