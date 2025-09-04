from fastapi import APIRouter, Path

from src.models.weather import WeatherRequest, WeatherResponse


router = APIRouter()


@router.get("/weather/{lat}/{lon}", tags=["weather"])
def weather(
    lat: float = Path(..., ge=-90, le=90, description="Latitude"),
    lon: float = Path(..., ge=-180, le=180, description="Longitude"),
) -> WeatherResponse:
    coordinates = WeatherRequest(latitude=lat, longitude=lon)

    return WeatherResponse(coordinates=coordinates, data=[])
