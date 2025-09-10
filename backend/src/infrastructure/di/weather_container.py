from src.application.services.weather_service import WeatherService
from src.infrastructure.services.command_adapter import CommandAdapter
from src.infrastructure.services.open_meteo import OpenMeteoAdapter
from src.infrastructure.services.query_adapter import QueryAdapter


def weather_service() -> WeatherService:
    query_adapter = QueryAdapter()
    command_adapter = CommandAdapter()

    api_adapter = OpenMeteoAdapter()
    return WeatherService(
        query_port=query_adapter, command_port=command_adapter, api_port=api_adapter
    )
