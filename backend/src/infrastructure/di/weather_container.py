from src.application.services.weather_service import WeatherService
from src.infrastructure.services.open_meteo import OpenMeteoAdapter


def weather_service() -> WeatherService:
    weather_adapter = OpenMeteoAdapter()
    return WeatherService(weather_adapter)
