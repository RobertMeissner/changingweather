from typing import Dict

from src.domain.entities.weather import WeatherCoordinate, WeatherData


class MockCommandAdapter:
    """Mock implementation of WeatherCommandPort for testing."""

    def __init__(self):
        # Store cached data in memory for verification
        self._cached_data: Dict[str, WeatherData] = {}

    def cache(self, data: WeatherData) -> None:
        """Store weather data in memory."""
        # Create a cache key based on coordinate
        key = f"{data.coordinate.latitude},{data.coordinate.longitude}"
        self._cached_data[key] = data

    def invalidate_cache(self, coordinate: WeatherCoordinate) -> None:
        """Remove weather data for a specific coordinate."""
        key = f"{coordinate.latitude},{coordinate.longitude}"
        self._cached_data.pop(key, None)

    # Test utility methods
    def get_cached_data(self, coordinate: WeatherCoordinate) -> WeatherData | None:
        """Get cached data for testing verification."""
        key = f"{coordinate.latitude},{coordinate.longitude}"
        return self._cached_data.get(key)

    def get_all_cached_data(self) -> Dict[str, WeatherData]:
        """Get all cached data for testing verification."""
        return self._cached_data.copy()

    def clear_cache(self) -> None:
        """Clear all cached data for test cleanup."""
        self._cached_data.clear()

    def get_cache_count(self) -> int:
        """Get number of cached entries for testing."""
        return len(self._cached_data)
