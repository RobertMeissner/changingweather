from datetime import datetime

from sqlmodel import Field

from src.models.base import BaseModel


class WeatherDataRecord(BaseModel, table=True):
    """SQLModel for persisting weather data in PostgreSQL"""

    __tablename__ = "weather_data"

    latitude: float = Field(index=True)
    longitude: float = Field(index=True)
    temperature: float = Field()
    timestamp: datetime = Field(index=True)

    class Config:
        arbitrary_types_allowed = True
