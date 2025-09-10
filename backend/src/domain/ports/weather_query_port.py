from typing import Protocol

import pandas as pd
import redis

from src.domain.entities.weather import WeatherData, WeatherQueryOptions


class WeatherQueryPort(Protocol):
    """

    Query port.
    Responsible to map repository model to API output model/read model WeatherData
    """

    def __init__(self, redis_client: redis.Redis): ...

    def fetch(self, options: WeatherQueryOptions) -> pd.DataFrame: ...

    def map(self, data: pd.DataFrame, options: WeatherQueryOptions) -> WeatherData: ...

    def get(self, options: WeatherQueryOptions) -> WeatherData: ...

    def cache(self, data: WeatherData, options: WeatherQueryOptions) -> None: ...
