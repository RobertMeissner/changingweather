from typing import Protocol

from src.domain.entities.weather import WeatherCoordinate, WeatherData


class WeatherCommandPort(Protocol):
    """

    Takes care of writing
    Contract with persistence model
    """

    def cache(self, data: WeatherData) -> None: ...
    def invalidate_cache(self, coordinate: WeatherCoordinate) -> None: ...

    # TODO: Log fetch, e.g., metadata, rate limis
