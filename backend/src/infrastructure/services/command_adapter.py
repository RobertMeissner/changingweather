from typing import Callable

from sqlalchemy.orm import Session

from src.domain.entities.weather import WeatherCoordinate, WeatherData
from src.models.weather_data import WeatherDataRecord


class CommandAdapter:
    """
    Implements WeatherCommandPort
    Handles writing weather data to db
    """

    def __init__(self, session_factory: Callable[[], Session]):
        self._session_factory = session_factory

    def cache(self, data: WeatherData) -> None:
        with self._session_factory() as session:
            weather_records = []
            for data_point in data.data:
                record = WeatherDataRecord(
                    latitude=data.coordinate.latitude,
                    longitude=data.coordinate.longitude,
                    temperature=data_point.temperature,
                    timestamp=data_point.timestamp,
                )
                weather_records.append(record)

            session.add_all(weather_records)
            session.commit()

    def invalidate_cache(self, coordinate: WeatherCoordinate) -> None:
        with self._session_factory() as session:
            session.query(WeatherDataRecord).filter(
                WeatherDataRecord.latitude == coordinate.latitude,
                WeatherDataRecord.longitude == coordinate.longitude,
            ).delete()
            session.commit()
