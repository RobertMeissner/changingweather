import pandas as pd
import redis

from src.domain.entities.weather import WeatherData, WeatherQueryOptions


class QueryAdapter:
    """

    Implements WeatherQueryPort
    """

    def __init__(self, redis_client: redis.Redis):
        self._redis = redis_client
        self._cache_ttl = 1800

    def fetch(self, options: WeatherQueryOptions) -> pd.DataFrame:
        return pd.DataFrame()

    def map(self, data: pd.DataFrame, options: WeatherQueryOptions) -> WeatherData:
        return WeatherData(coordinate=options.coordinate, data=[])

    def get(self, options: WeatherQueryOptions) -> WeatherData:
        cache_key = self._cache_key(options)

        try:
            cached_data = self._redis.get(cache_key)
            if cached_data:
                return self.map(cached_data, options)
        except redis.RedisError:
            pass

        return self.map(pd.DataFrame(), options)

    @staticmethod
    def _cache_key(options: WeatherQueryOptions) -> str:
        lat = round(options.coordinate.latitude, 2)  # about 1_000m accuracy
        lon = round(options.coordinate.longitude, 2)
        date_range = f"{options.start}:{options.end}"
        return f"{lat}:{lon}:{date_range}"

    def _serialize(self, options: WeatherData) -> str:
        return ""

    def cache(self, data: WeatherData, options: WeatherQueryOptions) -> None:
        self._redis.set(self._cache_key(options), self._serialize(data))
