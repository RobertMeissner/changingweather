from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class WeatherRequest(BaseModel):
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)

    @field_validator("latitude")
    @classmethod
    def validate_latitue(cls, value: float) -> float:
        if not (-90 <= value <= 90):
            raise ValueError("latitude must be between -90 and 90")
        return value

    @field_validator("longitude")
    @classmethod
    def validate_longitude(cls, value: float) -> float:
        if not (-180 <= value <= 180):
            raise ValueError("longitude must be between -180 and 180")
        return value


class WeatherDataPoint(BaseModel):
    timestamp: datetime
    temperature: float = Field(ge=-100, le=100)


class WeatherResponse(BaseModel):
    coordinates: WeatherRequest
    data: list[WeatherDataPoint]
