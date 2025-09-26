import os
from enum import Enum
from src.api.http_client import HttpClient


class Service(Enum):
    SOME_SERVICE = "some_service"


BASE_URLS = {
    Service.SOME_SERVICE: os.getenv("SOME_SERVICE_URL"),
}


class RequestsHttpClient(HttpClient):
    pass
