import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry

from src.domain.entities.weather import (
    WeatherData,
    WeatherDataPoint,
    WeatherQueryOptions,
)


class OpenMeteoAdapter:
    """
    Adapter for OpenMeteo historical weather api
    Implements WeatherApiPort

    API description: https://open-meteo.com/en/docs/historical-weather-api
    """

    url = "https://archive-api.open-meteo.com/v1/archive"

    def __init__(self):
        cache_session = requests_cache.CachedSession(".cache", expire_after=3600)
        retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
        self.openmeteo = openmeteo_requests.Client(session=retry_session)

    def fetch(self, options: WeatherQueryOptions) -> pd.DataFrame:
        params = {
            "latitude": options.coordinate.latitude,
            "longitude": options.coordinate.longitude,
            "start_date": options.start.strftime("%Y-%m-%d"),
            "end_date": options.end.strftime("%Y-%m-%d"),
            "hourly": ["temperature_2m"],
            # "current": ["temperature_2m", "relative_humidity_2m"],
        }
        locations = self.openmeteo.weather_api(self.url, params=params)
        location = locations[0]
        print(location)
        hourly = location.Hourly()
        hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()  # This gives you NumPy arrays
        hourly_data = {
            "date": pd.date_range(
                start=pd.to_datetime(hourly.Time(), unit="s"),
                end=pd.to_datetime(hourly.TimeEnd(), unit="s"),
                freq=pd.Timedelta(seconds=hourly.Interval()),
                inclusive="left",
            ),
            "temperature_2m": hourly_temperature_2m,
        }
        return pd.DataFrame(data=hourly_data)

    def map(self, data: pd.DataFrame, options: WeatherQueryOptions) -> WeatherData:
        weather_data_points = [
            WeatherDataPoint(temperature=row["temperature_2m"], timestamp=row["date"])
            for _, row in data.iterrows()
        ]
        return WeatherData(
            coordinate=options.coordinate,
            data=weather_data_points,
        )

    def get(self, options: WeatherQueryOptions) -> WeatherData:
        return self.map(self.fetch(options), options)
