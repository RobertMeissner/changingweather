from dataclasses import dataclass
from datetime import datetime


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
    coordinate: WeatherCoordinate
    data: list[WeatherDataPoint]
