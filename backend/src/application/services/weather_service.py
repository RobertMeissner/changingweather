from datetime import datetime, timedelta

from src.domain.entities.weather import WeatherCoordinate, WeatherData
from src.domain.ports.weather_port import WeatherPort


class WeatherService:
    def __init__(self, weather_adapter: WeatherPort):
        self._weather_adapter = weather_adapter

    def weather_for_location(
        self,
        coordinate: WeatherCoordinate,
        start: datetime | None = None,
        end: datetime | None = None,
    ) -> WeatherData:
        if start is None:
            start = datetime.now() - timedelta(days=7)
        if end is None:
            end = datetime.now()
        # TODO: Check whether coordinates are in database
        return self._weather_adapter.pulled_data(coordinate, start, end)
