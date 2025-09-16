from typing import Protocol

from src.domain.entities.weather import (
    WeatherData,
    WeatherDataPoint,
    WeatherQueryOptions,
)
from src.domain.ports.cache_port import CachePort


class WeatherQueryPort(Protocol):
    """

    Query port.
    Responsible to map repository model to API output model/read model WeatherData
    """

    def __init__(self, cache: CachePort): ...

    def map_to_model(
        self, data: list[WeatherDataPoint], options: WeatherQueryOptions
    ) -> WeatherData: ...

    def get(self, options: WeatherQueryOptions) -> WeatherData: ...

    def cache(self, data: WeatherData, options: WeatherQueryOptions) -> None: ...
