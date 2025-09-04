from datetime import datetime
from typing import Protocol

from src.domain.entities.weather import WeatherCoordinate, WeatherData


class WeatherPort(Protocol):
    def pulled_data(
        self, coordinate: WeatherCoordinate, start: datetime, end: datetime
    ) -> WeatherData: ...
