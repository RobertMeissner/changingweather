from src.domain.entities.weather import WeatherData, WeatherQueryOptions
from src.domain.ports.weather_api_port import WeatherApiPort
from src.domain.ports.weather_command_port import WeatherCommandPort
from src.domain.ports.weather_query_port import WeatherQueryPort


class WeatherService:
    """

    Manager, pulling it all together
    """

    def __init__(
        self,
        query_port: WeatherQueryPort,
        command_port: WeatherCommandPort,
        api_port: WeatherApiPort,
    ):
        self._query_port = query_port
        self._command_port = command_port
        self._api_port = api_port

    def weather_for_location(
        self,
        options: WeatherQueryOptions,
    ) -> WeatherData:
        # TODO: Check whether coordinates are in database
        #  Otherwise -> query API -> store data in db for future caching
        cached = self._query_port.get(options)
        if cached.data:
            return cached

        weather_data = self._api_port.get(options)

        self._command_port.cache(weather_data)
        self._query_port.cache(weather_data, options)
        return weather_data
