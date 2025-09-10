from src.domain.entities.weather import WeatherCoordinate, WeatherData


class CommandAdapter:
    """

    Implements WeatherCommandPort
    """

    def cache(self, data: WeatherData) -> None:
        pass

    def invalidate_cache(self, coordinate: WeatherCoordinate) -> None:
        pass
