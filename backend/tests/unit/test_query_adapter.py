import datetime

from src.domain.entities.weather import WeatherCoordinate, WeatherQueryOptions
from src.infrastructure.services.query_adapter import QueryAdapter


def test__cache_key():
    options = WeatherQueryOptions(
        coordinate=WeatherCoordinate(latitude=-10, longitude=10),
        start=datetime.date(2020, 1, 1),
        end=datetime.date(2020, 1, 2),
    )

    cached_key = QueryAdapter._cache_key(options)
    assert cached_key == "-10:10:2020-01-01:2020-01-02"
