import datetime

import pytest

from src.domain.entities.weather import (
    WeatherCoordinate,
    WeatherData,
    WeatherDataPoint,
    WeatherQueryOptions,
)
from src.infrastructure.services.query_adapter import QueryAdapter


def test__cache_key():
    options = WeatherQueryOptions(
        coordinate=WeatherCoordinate(latitude=-10, longitude=10),
        start=datetime.date(2020, 1, 1),
        end=datetime.date(2020, 1, 2),
    )

    cached_key = QueryAdapter._cache_key(options)
    assert cached_key == "-10:10:2020-01-01:2020-01-02"


@pytest.mark.parametrize(
    "data, expected",
    [
        ("[]", []),
        (
            '[{"temperature": 273.15, "timestamp": 1577833200.0}]',
            [WeatherDataPoint(temperature=273.15, timestamp=datetime.datetime(2020, 1, 1))],
        ),
        (
            '[{"temperature": 273.15, "timestamp": 1577833200.0}, {"temperature": 274.15, "timestamp": 1609455600.0}]',
            [
                WeatherDataPoint(temperature=273.15, timestamp=datetime.datetime(2020, 1, 1)),
                WeatherDataPoint(temperature=274.15, timestamp=datetime.datetime(2021, 1, 1)),
            ],
        ),
    ],
)
def test__deserialize(data, expected):
    assert QueryAdapter._deserialize(data) == expected


@pytest.mark.parametrize(
    "data, expected",
    [
        ([], "[]"),
        (
            [WeatherDataPoint(temperature=273.15, timestamp=datetime.datetime(2020, 1, 1))],
            '[{"temperature": 273.15, "timestamp": 1577833200.0}]',
        ),
        (
            [
                WeatherDataPoint(temperature=273.15, timestamp=datetime.datetime(2020, 1, 1)),
                WeatherDataPoint(temperature=274.15, timestamp=datetime.datetime(2021, 1, 1)),
            ],
            '[{"temperature": 273.15, "timestamp": 1577833200.0}, {"temperature": 274.15, "timestamp": 1609455600.0}]',
        ),
    ],
)
def test__serialize(data, expected):
    test_data = WeatherData(coordinate=WeatherCoordinate(latitude=-10, longitude=10), data=data)
    serialized = QueryAdapter._serialize(test_data)
    assert serialized == expected


def test_serialize_deserialize():
    coordinate = WeatherCoordinate(latitude=-10, longitude=10)
    data = WeatherData(
        coordinate=coordinate,
        data=[
            WeatherDataPoint(temperature=273.15, timestamp=datetime.datetime(2020, 1, 1)),
            WeatherDataPoint(temperature=274.15, timestamp=datetime.datetime(2021, 1, 1)),
        ],
    )
    assert QueryAdapter._deserialize(serialized_data=QueryAdapter._serialize(data)) == data.data


def test_roundtrip_serialize_deserialize():
    coordinate = WeatherCoordinate(latitude=-10, longitude=10)
    data = WeatherData(
        coordinate=coordinate,
        data=[
            WeatherDataPoint(temperature=273.15, timestamp=datetime.datetime(2020, 1, 1)),
            WeatherDataPoint(temperature=274.15, timestamp=datetime.datetime(2021, 1, 1)),
        ],
    )
    options = WeatherQueryOptions(
        coordinate=coordinate, start=datetime.date(2020, 1, 1), end=datetime.date(2020, 1, 2)
    )
    assert (
        QueryAdapter.map_to_model(
            data=QueryAdapter._deserialize(serialized_data=QueryAdapter._serialize(data)),
            options=options,
        )
        == data
    )
