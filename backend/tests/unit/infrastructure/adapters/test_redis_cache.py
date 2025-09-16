from unittest.mock import Mock

import redis

from src.infrastructure.adapters.redis_cache import RedisCache


class TestRedisCache:
    def test_get_success(self):
        mock_redis = Mock()
        mock_redis.get.return_value = b"test_value"

        cache = RedisCache(mock_redis)
        result = cache.get("test_key")

        assert result == "test_value"
        mock_redis.get.assert_called_once_with("test_key")

    def test_get_returns_none_when_key_not_found(self):
        mock_redis = Mock()
        mock_redis.get.return_value = None

        cache = RedisCache(mock_redis)
        result = cache.get("nonexistent_key")

        assert result is None

    def test_get_handles_redis_error_gracefully(self):
        mock_redis = Mock()
        mock_redis.get.side_effect = redis.RedisError("Connection failed")

        cache = RedisCache(mock_redis)
        result = cache.get("test_key")

        assert result is None

    def test_set_without_ttl(self):
        mock_redis = Mock()

        cache = RedisCache(mock_redis)
        cache.set("test_key", "test_value")

        mock_redis.set.assert_called_once_with("test_key", "test_value")

    def test_set_with_ttl(self):
        mock_redis = Mock()

        cache = RedisCache(mock_redis)
        cache.set("test_key", "test_value", ttl=3600)

        mock_redis.setex.assert_called_once_with("test_key", 3600, "test_value")

    def test_set_handles_redis_error_gracefully(self):
        mock_redis = Mock()
        mock_redis.set.side_effect = redis.RedisError("Connection failed")

        cache = RedisCache(mock_redis)

        # Should not raise exception
        cache.set("test_key", "test_value")

    def test_set_with_ttl_handles_redis_error_gracefully(self):
        mock_redis = Mock()
        mock_redis.setex.side_effect = redis.RedisError("Connection failed")

        cache = RedisCache(mock_redis)

        # Should not raise exception
        cache.set("test_key", "test_value", ttl=3600)

    def test_delete_success(self):
        mock_redis = Mock()

        cache = RedisCache(mock_redis)
        cache.delete("test_key")

        mock_redis.delete.assert_called_once_with("test_key")

    def test_delete_handles_redis_error_gracefully(self):
        mock_redis = Mock()
        mock_redis.delete.side_effect = redis.RedisError("Connection failed")

        cache = RedisCache(mock_redis)

        # Should not raise exception
        cache.delete("test_key")

    def test_unicode_handling(self):
        mock_redis = Mock()
        mock_redis.get.return_value = "café".encode("utf-8")

        cache = RedisCache(mock_redis)
        result = cache.get("unicode_key")

        assert result == "café"

    def test_binary_data_decoding(self):
        mock_redis = Mock()
        mock_redis.get.return_value = b'{"temperature": 25.5}'

        cache = RedisCache(mock_redis)
        result = cache.get("json_key")

        assert result == '{"temperature": 25.5}'
