from dataclasses import dataclass
from datetime import date, datetime


@dataclass
class WeatherCoordinate:
    latitude: float
    longitude: float


@dataclass
class WeatherDataPoint:
    temperature: float
    timestamp: datetime


@dataclass
class WeatherData:
    # Todo: coordinate as part of WeatherData when persisting
    coordinate: WeatherCoordinate
    data: list[WeatherDataPoint]


@dataclass
class WeatherQueryOptions:
    coordinate: WeatherCoordinate
    start: date
    end: date
