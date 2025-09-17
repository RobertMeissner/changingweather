from datetime import datetime

from src.domain.entities.weather import WeatherCoordinate, WeatherData, WeatherDataPoint
from tests.mocks.mock_command_adapter import MockCommandAdapter


class TestCommandAdapter:
    """Test suite for command adapter functionality."""

    def setup_method(self):
        """Set up test fixtures before each test."""
        self.command_adapter = MockCommandAdapter()
        self.test_coordinate = WeatherCoordinate(latitude=1.5, longitude=2.5)
        self.test_data = WeatherData(
            coordinate=self.test_coordinate,
            data=[
                WeatherDataPoint(temperature=25.0, timestamp=datetime(2024, 1, 1, 12, 0)),
                WeatherDataPoint(temperature=26.5, timestamp=datetime(2024, 1, 1, 13, 0)),
            ],
        )

    def test_cache_stores_weather_data(self):
        """Test that cache method stores weather data correctly."""
        # Initially no data should be cached
        assert self.command_adapter.get_cache_count() == 0

        # Cache the test data
        self.command_adapter.cache(self.test_data)

        # Verify data was stored
        assert self.command_adapter.get_cache_count() == 1
        cached_data = self.command_adapter.get_cached_data(self.test_coordinate)

        assert cached_data is not None
        assert cached_data.coordinate.latitude == 1.5
        assert cached_data.coordinate.longitude == 2.5
        assert len(cached_data.data) == 2
        assert cached_data.data[0].temperature == 25.0

    def test_cache_overwrites_existing_data(self):
        """Test that caching new data for same coordinate overwrites existing data."""
        # Cache initial data
        self.command_adapter.cache(self.test_data)
        assert self.command_adapter.get_cache_count() == 1

        # Create new data for same coordinate
        new_data = WeatherData(
            coordinate=self.test_coordinate,
            data=[WeatherDataPoint(temperature=30.0, timestamp=datetime(2024, 1, 2, 12, 0))],
        )

        # Cache new data
        self.command_adapter.cache(new_data)

        # Should still have only one entry, but with new data
        assert self.command_adapter.get_cache_count() == 1
        cached_data = self.command_adapter.get_cached_data(self.test_coordinate)
        assert len(cached_data.data) == 1
        assert cached_data.data[0].temperature == 30.0

    def test_invalidate_cache_removes_data(self):
        """Test that invalidate_cache removes data for specified coordinate."""
        # Cache data first
        self.command_adapter.cache(self.test_data)
        assert self.command_adapter.get_cached_data(self.test_coordinate) is not None

        # Invalidate cache
        self.command_adapter.invalidate_cache(self.test_coordinate)

        # Verify data was removed
        assert self.command_adapter.get_cached_data(self.test_coordinate) is None
        assert self.command_adapter.get_cache_count() == 0

    def test_invalidate_cache_nonexistent_coordinate(self):
        """Test that invalidating non-existent coordinate doesn't raise error."""
        # Try to invalidate cache for coordinate that was never cached
        nonexistent_coord = WeatherCoordinate(latitude=99.0, longitude=99.0)

        # This should not raise an error
        self.command_adapter.invalidate_cache(nonexistent_coord)
        assert self.command_adapter.get_cache_count() == 0

    def test_multiple_coordinates_cached_separately(self):
        """Test that different coordinates are cached as separate entries."""
        coord1 = WeatherCoordinate(latitude=1.0, longitude=1.0)
        coord2 = WeatherCoordinate(latitude=2.0, longitude=2.0)

        data1 = WeatherData(
            coordinate=coord1,
            data=[WeatherDataPoint(temperature=20.0, timestamp=datetime(2024, 1, 1, 12, 0))],
        )
        data2 = WeatherData(
            coordinate=coord2,
            data=[WeatherDataPoint(temperature=25.0, timestamp=datetime(2024, 1, 1, 12, 0))],
        )

        # Cache both datasets
        self.command_adapter.cache(data1)
        self.command_adapter.cache(data2)

        # Verify both are cached separately
        assert self.command_adapter.get_cache_count() == 2

        cached1 = self.command_adapter.get_cached_data(coord1)
        cached2 = self.command_adapter.get_cached_data(coord2)

        assert cached1 is not None
        assert cached2 is not None
        assert cached1.data[0].temperature == 20.0
        assert cached2.data[0].temperature == 25.0

    def test_clear_cache_removes_all_data(self):
        """Test that clear_cache removes all cached data."""
        # Cache multiple datasets
        coord1 = WeatherCoordinate(latitude=1.0, longitude=1.0)
        coord2 = WeatherCoordinate(latitude=2.0, longitude=2.0)

        self.command_adapter.cache(WeatherData(coordinate=coord1, data=[]))
        self.command_adapter.cache(WeatherData(coordinate=coord2, data=[]))

        assert self.command_adapter.get_cache_count() == 2

        # Clear all cache
        self.command_adapter.clear_cache()

        # Verify all data is removed
        assert self.command_adapter.get_cache_count() == 0
        assert self.command_adapter.get_cached_data(coord1) is None
        assert self.command_adapter.get_cached_data(coord2) is None

    def test_get_all_cached_data(self):
        """Test that get_all_cached_data returns copy of all cached data."""
        # Cache some data
        self.command_adapter.cache(self.test_data)

        all_data = self.command_adapter.get_all_cached_data()

        assert len(all_data) == 1
        assert "1.5,2.5" in all_data
        assert all_data["1.5,2.5"].coordinate.latitude == 1.5

        # Verify it's a copy (modifying returned dict doesn't affect cache)
        all_data.clear()
        assert self.command_adapter.get_cache_count() == 1
