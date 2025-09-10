import pandas as pd

from src.domain.entities.weather import WeatherData, WeatherQueryOptions


class QueryAdapter:
    """

    Implements WeatherQueryPort
    """

    def fetch(self, options: WeatherQueryOptions) -> pd.DataFrame:
        return pd.DataFrame()

    def map(self, data: pd.DataFrame, options: WeatherQueryOptions) -> WeatherData:
        return WeatherData(coordinate=options.coordinate, data=[])

    def get(self, options: WeatherQueryOptions) -> WeatherData:
        return self.map(self.fetch(options), options)
