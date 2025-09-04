from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.api.v1.weather import router


test_app = FastAPI()
test_app.include_router(router)
client = TestClient(test_app)


# TODO: to be replaced by bruno tests
def test_weather():
    response = client.get("/weather/1/1")
    assert response.json()["data"][0]["temperature"] == 1
