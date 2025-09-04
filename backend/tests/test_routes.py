from unittest.mock import MagicMock

from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.api.v1.health import router


# Create minimal app just for testing
test_app = FastAPI()
test_app.include_router(router)
client = TestClient(test_app)


def test_health(monkeypatch: MagicMock):
    monkeypatch.setenv("POSTGRES_USER", "test")
    monkeypatch.setenv("POSTGRES_PASSWORD", "test")
    monkeypatch.setenv("POSTGRES_DB", "test")
    monkeypatch.setenv("POSTGRES_HOST", "localhost")

    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"ping": "pong!"}
