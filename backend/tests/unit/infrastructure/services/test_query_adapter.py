import datetime
import json
from datetime import date

import pytest

from src.domain.entities.weather import (
    WeatherCoordinate,
    WeatherData,
    WeatherDataPoint,
    WeatherQueryOptions,
)
from src.infrastructure.services.query_adapter import QueryAdapter
from tests.mocks.mock_cache import MockCache


@pytest.fixture
def mock_cache():
    return MockCache()


class TestQueryAdapter:
    def test__cache_key(self):
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
                '[{"temperature": 273.15, "timestamp": 1577836800.0}]',
                [WeatherDataPoint(temperature=273.15, timestamp=datetime.datetime(2020, 1, 1))],
            ),
            (
                '[{"temperature": 273.15, "timestamp": 1577836800.0}, {"temperature": 274.15, "timestamp": 1609459200.0}]',
                [
                    WeatherDataPoint(temperature=273.15, timestamp=datetime.datetime(2020, 1, 1)),
                    WeatherDataPoint(temperature=274.15, timestamp=datetime.datetime(2021, 1, 1)),
                ],
            ),
        ],
    )
    def test__deserialize(self, data, expected):
        assert QueryAdapter._deserialize(data) == expected

    @pytest.mark.parametrize(
        "data, expected",
        [
            ([], "[]"),
            (
                [WeatherDataPoint(temperature=273.15, timestamp=datetime.datetime(2020, 1, 1))],
                '[{"temperature": 273.15, "timestamp": 1577836800.0}]',
            ),
            (
                [
                    WeatherDataPoint(temperature=273.15, timestamp=datetime.datetime(2020, 1, 1)),
                    WeatherDataPoint(temperature=274.15, timestamp=datetime.datetime(2021, 1, 1)),
                ],
                '[{"temperature": 273.15, "timestamp": 1577836800.0}, {"temperature": 274.15, "timestamp": 1609459200.0}]',
            ),
        ],
    )
    def test__serialize(self, data, expected):
        test_data = WeatherData(coordinate=WeatherCoordinate(latitude=-10, longitude=10), data=data)
        serialized = QueryAdapter._serialize(test_data)
        assert serialized == expected

    def test_serialize_deserialize(self):
        coordinate = WeatherCoordinate(latitude=-10, longitude=10)
        data = WeatherData(
            coordinate=coordinate,
            data=[
                WeatherDataPoint(temperature=273.15, timestamp=datetime.datetime(2020, 1, 1)),
                WeatherDataPoint(temperature=274.15, timestamp=datetime.datetime(2021, 1, 1)),
            ],
        )
        assert QueryAdapter._deserialize(serialized_data=QueryAdapter._serialize(data)) == data.data

    def test_roundtrip_serialize_deserialize(self):
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

    def test_cache_miss_returns_empty_weather_data(self, mock_cache):
        adapter = QueryAdapter(cache=mock_cache)

        options = WeatherQueryOptions(
            coordinate=WeatherCoordinate(latitude=1.0, longitude=2.0),
            start=date(2020, 1, 1),
            end=date(2020, 1, 2),
        )

        result = adapter.get(options)

        assert result.coordinate == options.coordinate
        assert result.data == []

    def test_cache_hit_returns_deserialized_data(self, mock_cache):
        adapter = QueryAdapter(cache=mock_cache)

        # Prepare test data
        options = WeatherQueryOptions(
            coordinate=WeatherCoordinate(latitude=1.0, longitude=2.0),
            start=date(2020, 1, 1),
            end=date(2020, 1, 2),
        )

        test_timestamp = datetime.datetime(2020, 1, 1, 12, 0)
        cached_data = json.dumps(
            [
                {
                    "temperature": 25.5,
                    "timestamp": test_timestamp.replace(tzinfo=datetime.timezone.utc).timestamp(),
                }
            ]
        )

        cache_key = adapter._cache_key(options)
        mock_cache.set(cache_key, cached_data)

        result = adapter.get(options)

        assert result.coordinate == options.coordinate
        assert len(result.data) == 1
        assert result.data[0].temperature == 25.5
        assert result.data[0].timestamp == test_timestamp

    def test_cache_key_generation_consistent(self, mock_cache):
        adapter = QueryAdapter(cache=mock_cache)

        options = WeatherQueryOptions(
            coordinate=WeatherCoordinate(latitude=1.12345, longitude=2.67890),
            start=date(2020, 1, 1),
            end=date(2020, 1, 2),
        )

        key1 = adapter._cache_key(options)
        key2 = adapter._cache_key(options)

        assert key1 == key2
        assert key1 == "1.12:2.68:2020-01-01:2020-01-02"

    def test_cache_key_rounds_coordinates(self, mock_cache):
        adapter = QueryAdapter(cache=mock_cache)

        options = WeatherQueryOptions(
            coordinate=WeatherCoordinate(latitude=1.126, longitude=2.674),
            start=date(2020, 1, 1),
            end=date(2020, 1, 2),
        )

        key = adapter._cache_key(options)
        assert key == "1.13:2.67:2020-01-01:2020-01-02"

    def test_serialization_round_trip(self, mock_cache):
        adapter = QueryAdapter(cache=mock_cache)

        original_data = WeatherData(
            coordinate=WeatherCoordinate(latitude=1.0, longitude=2.0),
            data=[
                WeatherDataPoint(temperature=20.5, timestamp=datetime.datetime(2020, 1, 1, 12, 0)),
                WeatherDataPoint(temperature=22.0, timestamp=datetime.datetime(2020, 1, 1, 13, 0)),
            ],
        )

        serialized = adapter._serialize(original_data)
        deserialized_list = adapter._deserialize(serialized)

        assert len(deserialized_list) == 2
        assert deserialized_list[0].temperature == 20.5
        assert deserialized_list[0].timestamp == datetime.datetime(2020, 1, 1, 12, 0)
        assert deserialized_list[1].temperature == 22.0
        assert deserialized_list[1].timestamp == datetime.datetime(2020, 1, 1, 13, 0)

    def test_cache_stores_serialized_data(self, mock_cache):
        adapter = QueryAdapter(cache=mock_cache)

        options = WeatherQueryOptions(
            coordinate=WeatherCoordinate(latitude=1.0, longitude=2.0),
            start=date(2020, 1, 1),
            end=date(2020, 1, 2),
        )

        weather_data = WeatherData(
            coordinate=options.coordinate,
            data=[
                WeatherDataPoint(temperature=25.0, timestamp=datetime.datetime(2020, 1, 1, 12, 0))
            ],
        )

        adapter.cache(weather_data, options)

        cache_key = adapter._cache_key(options)
        cached_value = mock_cache.get(cache_key)

        assert cached_value is not None
        deserialized = adapter._deserialize(cached_value)
        assert len(deserialized) == 1
        assert deserialized[0].temperature == 25.0
