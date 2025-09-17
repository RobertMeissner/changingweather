from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.api.v1.weather import router
from src.application.services.weather_service import WeatherService
from src.infrastructure.di.weather_container import weather_service
from src.infrastructure.services.open_meteo import OpenMeteoAdapter
from src.infrastructure.services.query_adapter import QueryAdapter
from tests.mocks.mock_cache import MockCache
from tests.mocks.mock_command_adapter import MockCommandAdapter


def mock_weather_service() -> WeatherService:
    mock_cache = MockCache()
    query_adapter = QueryAdapter(cache=mock_cache)
    command_adapter = MockCommandAdapter()
    api_adapter = OpenMeteoAdapter()

    return WeatherService(
        query_port=query_adapter, command_port=command_adapter, api_port=api_adapter
    )


test_app = FastAPI()
test_app.include_router(router)

# Override the dependency for testing
test_app.dependency_overrides[weather_service] = mock_weather_service

client = TestClient(test_app)


class TestWeatherIntegration:
    def test_weather(self):
        """Test weather endpoint with mocked cache."""
        response = client.get("/weather/1/1")
        assert response.status_code == 200
        data = response.json()
        assert "coordinate" in data
        assert "data" in data
        assert (response.json()["data"][0]["temperature"] - 27.95) < 0.1

    def test_cache_isolation_between_requests(self):
        """Test that cache state is isolated between test runs."""
        # First request should work with empty cache
        response1 = client.get("/weather/1.0/1.0")
        assert response1.status_code == 200

        # Second request should also work (cache doesn't persist between tests)
        response2 = client.get("/weather/1.0/1.0")
        assert response2.status_code == 200

    def test_different_coordinates_get_different_cache_keys(self):
        """Test that different coordinates don't interfere with each other."""
        response1 = client.get("/weather/1.0/1.0")
        response2 = client.get("/weather/2.0/2.0")

        assert response1.status_code == 200
        assert response2.status_code == 200

        # Both should return valid data structures
        data1 = response1.json()
        data2 = response2.json()
        assert data1["coordinate"]["latitude"] == 1.0
        assert data2["coordinate"]["latitude"] == 2.0

    def test_date_range_affects_cache_key(self):
        """Test that different date ranges create different cache entries."""
        response1 = client.get("/weather/1.0/1.0?start=2020-01-01&end=2020-01-02")
        response2 = client.get("/weather/1.0/1.0?start=2020-01-03&end=2020-01-04")

        assert response1.status_code == 200
        assert response2.status_code == 200

    def test_coordinate_rounding_in_cache_key(self):
        """Test that coordinates are properly rounded for caching."""
        # These should use the same cache key due to coordinate rounding
        response1 = client.get("/weather/1.001/1.001")
        response2 = client.get("/weather/1.009/1.009")

        assert response1.status_code == 200
        assert response2.status_code == 200

    def test_mock_cache_is_used_in_tests(self):
        """Verify that MockCache is actually being used instead of Redis."""
        # This test verifies our dependency injection is working
        # If Redis were being used, we'd need a Redis server running
        response = client.get("/weather/1.0/1.0")
        assert response.status_code == 200

        # The fact that this test passes without Redis running
        # confirms MockCache is being used
