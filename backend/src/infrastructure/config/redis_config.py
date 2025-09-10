import os

import redis


class RedisConfig:
    def __init__(self):
        self.host = os.getenv("REDIS_HOST", "localhost")
        self.port = os.getenv("REDIS_PORT", 6380)
        self.db = os.getenv("REDIS_DB", 0)
        self.password = os.getenv("REDIS_PASSWORD", "")

    def client(self) -> redis.Redis:
        return redis.Redis(
            host=self.host,
            port=self.port,
            db=self.db,
            password=self.password,
            decode_responses=False,
            socket_timeout=5,
            socket_connect_timeout=5,
        )
