from datetime import datetime

from pydantic import BaseModel, Field

from src.domain.entities.weather import WeatherCoordinate


class WeatherDataPoint(BaseModel):
    timestamp: datetime
    temperature: float = Field(ge=-100, le=100)


class WeatherResponse(BaseModel):
    coordinate: WeatherCoordinate
    data: list[WeatherDataPoint]
