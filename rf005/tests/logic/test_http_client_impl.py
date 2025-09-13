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


def test_get_post_success_builds_url_and_returns_post(monkeypatch):
    called = {}

    def fake_request(method, url, json=None, headers=None, timeout=None):
        called["method"] = method
        called["url"] = url
        called["headers"] = headers
        now = datetime(2025, 1, 1, tzinfo=timezone.utc)
        data = {
            "id": str(pid),
            "route_id": str(uuid.uuid4()),
            "user_id": str(uuid.uuid4()),
            "created_at": now,
            "expire_at": now,
        }
        return DummyResponse(200, data)

    pid = uuid.uuid4()
    BASE_URLS[Service.POSTS] = "http://posts.local/posts"
    monkeypatch.setattr("src.api.impl.http_client.httpx.request", fake_request)

    client = RequestsHttpClient()
    token = "abc"
    post = client.get_post(pid, token)

    assert called["method"] == "GET"
    assert called["url"].endswith(str(pid))
    assert "Authorization" in called["headers"]
    assert post.id == str(pid) or str(post.id) == str(pid)


def test_get_offers_success_returns_list(monkeypatch):
    def fake_request(method, url, json=None, headers=None, timeout=None):
        now = datetime(2025, 1, 2, tzinfo=timezone.utc)
        data = [
            {
                "id": str(uuid.uuid4()),
                "post_id": str(oid),
                "user_id": str(uuid.uuid4()),
                "description": "Test",
                "size": OfferSize.SMALL,  # constructor expects Enum instance
                "fragile": False,
                "offer": 12.5,
                "created_at": now,
            }
        ]
        return DummyResponse(200, data)

    oid = uuid.uuid4()
    BASE_URLS[Service.OFFERS] = "http://offers.local/offers"
    monkeypatch.setattr("src.api.impl.http_client.httpx.request", fake_request)

    client = RequestsHttpClient()
    token = "abc"
    offers = client.get_offers(oid, token)
    assert len(offers) == 1
    assert str(offers[0].post_id) == str(oid)
    assert offers[0].size is OfferSize.SMALL


def test_get_route_404_maps_not_found(monkeypatch):
    def fake_request(method, url, json=None, headers=None, timeout=None):
        return DummyResponse(404, {}, content=b"not found")

    rid = uuid.uuid4()
    BASE_URLS[Service.ROUTES] = "http://routes.local/routes"
    monkeypatch.setattr("src.api.impl.http_client.httpx.request", fake_request)

    client = RequestsHttpClient()
    with pytest.raises(ApiException) as ei:
        client.get_route(rid, "abc")
    assert ei.value.type is ApiExceptionType.NOT_FOUND


def test_missing_base_url_raises_service_unavailable(monkeypatch):
    def fake_request(method, url, json=None, headers=None, timeout=None):
        return DummyResponse(200, {})

    # Ensure POSTS base URL is missing
    BASE_URLS[Service.POSTS] = None
    monkeypatch.setattr("src.api.impl.http_client.httpx.request", fake_request)

    client = RequestsHttpClient()
    with pytest.raises(ApiException) as ei:
        client.get_post(uuid.uuid4(), "abc")
    assert ei.value.type is ApiExceptionType.SERVICE_UNAVAILABLE


def test_generic_500_maps_service_unavailable(monkeypatch):
    def fake_request(method, url, json=None, headers=None, timeout=None):
        return DummyResponse(500, {}, content=b"oops")

    BASE_URLS[Service.POSTS] = "http://posts.local/posts"
    monkeypatch.setattr("src.api.impl.http_client.httpx.request", fake_request)

    client = RequestsHttpClient()
    with pytest.raises(ApiException) as ei:
        client.get_post(uuid.uuid4(), "abc")
    assert ei.value.type is ApiExceptionType.SERVICE_UNAVAILABLE


def test_get_user_info_calls_users_me(monkeypatch):
    captured = {}

    def fake_request(method, url, json=None, headers=None, timeout=None):
        captured["url"] = url
        data = {
            "id": str(uuid.uuid4()),
            "username": "user1",
            "email": "user1@example.com",
            "full_name": "User One",
            "dni": "123",
            "phone_number": "555",
            "status": "VERIFICADO",
        }
        return DummyResponse(200, data)

    BASE_URLS[Service.USERS] = "http://users.local/users"
    monkeypatch.setattr("src.api.impl.http_client.httpx.request", fake_request)

    client = RequestsHttpClient()
    user = client.get_user_info("abc")
    assert captured["url"].endswith("/me")
    assert user.username == "user1"
