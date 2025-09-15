import uuid
from datetime import datetime, timezone

import pytest

from src.api.impl.http_client import BASE_URLS, RequestsHttpClient, Service
from src.exceptions.api_exception import ApiException, ApiExceptionType
from src.models.internal.offer import OfferSize


class DummyResponse:
    def __init__(self, status_code: int, data, content: bytes | None = None):
        self.status_code = status_code
        self._data = data
        self.content = (
            content if content is not None else (b"{}" if status_code == 200 else b"")
        )

    def json(self):
        return self._data


def test_get_route_503_maps_not_found(monkeypatch):
    def fake_request(method, url, json=None, headers=None, timeout=None):
        return DummyResponse(404, {}, content=b"not found")

    rid = uuid.uuid4()
    BASE_URLS[Service.ROUTES] = "http://routes.local/routes"
    monkeypatch.setattr("src.api.impl.http_client.httpx.request", fake_request)

    client = RequestsHttpClient()
    with pytest.raises(ApiException) as ei:
        client.get_route(rid, "abc")
    assert ei.value.type is ApiExceptionType.NOT_FOUND


def test_generic_500_maps_service_unavailable(monkeypatch):
    def fake_request(method, url, json=None, headers=None, timeout=None):
        return DummyResponse(500, {}, content=b"oops")

    BASE_URLS[Service.POSTS] = "http://posts.local/posts"
    monkeypatch.setattr("src.api.impl.http_client.httpx.request", fake_request)

    client = RequestsHttpClient()
    with pytest.raises(ApiException) as ei:
        client.get_post(uuid.uuid4(), "abc")
    assert ei.value.type is ApiExceptionType.SERVICE_UNAVAILABLE
