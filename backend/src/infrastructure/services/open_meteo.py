import datetime

from src.domain.entities.weather import WeatherCoordinate, WeatherData, WeatherDataPoint


class OpenMeteoAdapter:
    def pulled_data(
        self, coordinate: WeatherCoordinate, start: datetime, end: datetime
    ) -> WeatherData:
        return WeatherData(
            coordinate=coordinate, data=[WeatherDataPoint(timestamp=start, temperature=1)]
        )
