from src.application.services.weather_service import WeatherService
from src.infrastructure.adapters.redis_cache import RedisCache
from src.infrastructure.config.redis_config import RedisConfig
from src.infrastructure.services.command_adapter import CommandAdapter
from src.infrastructure.services.open_meteo import OpenMeteoAdapter
from src.infrastructure.services.query_adapter import QueryAdapter


def weather_service() -> WeatherService:
    from src.db.session import SessionLocal

    redis_config = RedisConfig()
    redis_client = redis_config.client()
    cache = RedisCache(redis_client)

    query_adapter = QueryAdapter(cache=cache)
    command_adapter = CommandAdapter(session_factory=SessionLocal)

    api_adapter = OpenMeteoAdapter()

    return WeatherService(
        query_port=query_adapter, command_port=command_adapter, api_port=api_adapter
    )
