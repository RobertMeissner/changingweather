import json
from datetime import datetime

import pandas as pd
import redis

from src.domain.entities.weather import (
    WeatherData,
    WeatherDataPoint,
    WeatherQueryOptions,
)


class QueryAdapter:
    """

    Implements WeatherQueryPort
    """

    def __init__(self, redis_client: redis.Redis):
        self._redis = redis_client
        self._cache_ttl = 1800

    def fetch(self, options: WeatherQueryOptions) -> pd.DataFrame:
        return pd.DataFrame()

    @staticmethod
    def map_to_model(data: list[WeatherDataPoint], options: WeatherQueryOptions) -> WeatherData:
        return WeatherData(coordinate=options.coordinate, data=data)

    def get(self, options: WeatherQueryOptions) -> WeatherData:
        cache_key = self._cache_key(options)

        try:
            cached_data = self._redis.get(cache_key)
            if cached_data:
                return self.map_to_model(
                    data=self._deserialize(cached_data.decode("utf-8"), options.coordinate),
                    options=options,
                )
        except redis.RedisError:
            pass

        return self.map_to_model(pd.DataFrame(), options)

    @staticmethod
    def _cache_key(options: WeatherQueryOptions) -> str:
        lat = round(options.coordinate.latitude, 2)  # about 1_000m accuracy
        lon = round(options.coordinate.longitude, 2)
        date_range = f"{options.start}:{options.end}"
        return f"{lat}:{lon}:{date_range}"

    @staticmethod
    def _deserialize(serialized_data: str) -> list[WeatherDataPoint]:
        data_points = json.loads(serialized_data)
        return [
            WeatherDataPoint(
                temperature=point["temperature"],
                timestamp=datetime.fromtimestamp(point["timestamp"]),
            )
            for point in data_points
        ]

    @staticmethod
    def _serialize(data: WeatherData) -> str:
        return json.dumps(
            [
                {"temperature": point.temperature, "timestamp": point.timestamp.timestamp()}
                for point in data.data
            ]
        )

    def cache(self, data: WeatherData, options: WeatherQueryOptions) -> None:
        raise NotImplementedError()
        self._redis.set(self._cache_key(options), self._serialize(data))
