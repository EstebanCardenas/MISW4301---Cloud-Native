from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.api.http_server import router

app = FastAPI()
app.include_router(router)
client = TestClient(app)


def test_ping():
    response = client.get("/posts/ping")
    assert response.status_code == 200
    assert response.json() == "pong"
