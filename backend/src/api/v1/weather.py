import datetime
import logging
from typing import Optional

from fastapi import APIRouter, Depends, Path, Query

from src.application.services.weather_service import WeatherService
from src.domain.entities.weather import WeatherCoordinate, WeatherQueryOptions
from src.infrastructure.di.weather_container import weather_service
from src.models.weather import WeatherDataPoint, WeatherResponse


router = APIRouter()

logger = logging.getLogger(__name__)


@router.get("/weather/{lat}/{lon}", tags=["weather"])
def weather(
    lat: float = Path(..., ge=-90, le=90, description="Latitude"),
    lon: float = Path(..., ge=-180, le=180, description="Longitude"),
    start: Optional[datetime.datetime] = Query(
        datetime.datetime(2020, 1, 1), description="Start date (YYYY-MM-DD)"
    ),
    end: Optional[datetime.datetime] = Query(
        datetime.datetime(2020, 1, 2), description="End date (YYYY-MM-DD)"
    ),
    service: WeatherService = Depends(weather_service),
) -> WeatherResponse:
    # TODO: Naming, in = query, out = response
    options = WeatherQueryOptions(
        coordinate=WeatherCoordinate(latitude=lat, longitude=lon),
        start=start,
        end=end,
    )
    weather_data = service.weather_for_location(options)
    logger.debug(f"weather_data: {weather_data}")
    return WeatherResponse(
        coordinate=options.coordinate,
        data=[
            WeatherDataPoint(timestamp=data.timestamp, temperature=data.temperature)
            for data in weather_data.data
        ],
    )
