import datetime

from src.domain.entities.weather import WeatherCoordinate, WeatherQueryOptions
from src.infrastructure.services.open_meteo import OpenMeteoAdapter


def test_get_data():
    coordinate = WeatherCoordinate(latitude=45.0, longitude=-122.0)
    open_meteo_adapter = OpenMeteoAdapter()

    options = WeatherQueryOptions(
        coordinate=coordinate,
        start=datetime.datetime(2020, 1, 1),
        end=datetime.datetime(2020, 1, 2),
    )
    response = open_meteo_adapter.get(options)
    assert response.coordinate == coordinate
    assert len(response.data) == 2 * 24
    assert response.data[0].timestamp == datetime.datetime(2020, 1, 1)
    assert abs(response.data[0].temperature - 3.67) < 0.1


# def
