import time
import uuid
from datetime import datetime, timedelta
from typing import Any, Optional
from unittest.mock import Mock, patch

import pytest
import requests
from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


@pytest.fixture
def mock_requests_factory():

    def _factory(
        method: str,
        responses: list[tuple[int, dict[str, Any]]],
        simulate_timeout_per_request: Optional[list[bool]] = None,
    ):
        def mock_request(url, *args, **kwargs):
            if simulate_timeout_per_request and simulate_timeout_per_request.pop(0):
                raise requests.Timeout("Simulated timeout")
            mock_response = Mock()
            status_code, json_data = responses.pop(0)
            mock_response.status_code = status_code
            mock_response.json.return_value = json_data or {}
            return mock_response

        return patch(f"requests.{method}", side_effect=mock_request)

    return _factory


def test_create_offer_incomplete_invalid():
    request_data = {"description": "Test Offer", "size": "Medium", "fragile": False}
    response = client.post(
        f"/rf004/posts/{uuid.uuid4()}/offers",
        json=request_data,
        headers={"Authorization": f"Bearer {uuid.uuid4()}"},
    )
    assert response.status_code == 400


def test_create_offer_no_auth_token(mock_requests_factory):
    with mock_requests_factory(
        "get",
        [
            (
                403,
                {"detail": "Authorization token is missing"},
            )
        ],
    ):
        request_data = {
            "description": "Test Offer",
            "size": "Medium",
            "fragile": False,
            "offer": 99.99,
        }
        response = client.post(f"/rf004/posts/{uuid.uuid4()}/offers", json=request_data)
        assert response.status_code == 403


def test_create_offer_expired_auth_token(mock_requests_factory):
    with mock_requests_factory(
        "get",
        [
            (
                401,
                {"detail": "Token has expired"},
            )
        ],
    ):
        request_data = {
            "description": "Test Offer",
            "size": "Medium",
            "fragile": False,
            "offer": 99.99,
        }
        response = client.post(
            f"/rf004/posts/{uuid.uuid4()}/offers",
            json=request_data,
            headers={"Authorization": f"Bearer {uuid.uuid4()}"},
        )
        assert response.status_code == 401


def test_create_offer_post_doesnt_exist(mock_requests_factory):
    with mock_requests_factory(
        "get",
        [
            (
                200,
                {
                    "id": str(uuid.uuid4()),
                    "username": "test-user",
                    "email": "testuser@example.com",
                    "fullName": "Test User Fullname",
                    "dni": "12345678",
                    "phoneNumber": "1234567890",
                    "status": "VERIFICADO",
                },
            ),
            (200, "pong"),
            (404, {"detail": "Post not found"}),
        ],
    ):
        request_data = {
            "description": "Test Offer",
            "size": "MEDIUM",
            "fragile": False,
            "offer": 99.99,
        }
        response = client.post(
            f"/rf004/posts/{uuid.uuid4()}/offers",
            json=request_data,
            headers={"Authorization": f"Bearer {uuid.uuid4()}"},
        )
        assert response.status_code == 404


def test_create_offer_post_is_from_same_user(mock_requests_factory):
    user_id = uuid.uuid4()
    post_id = uuid.uuid4()

    with mock_requests_factory(
        "get",
        [
            (
                200,
                {
                    "id": str(user_id),
                    "username": "test-user",
                    "email": "testuser@example.com",
                    "fullName": "Test User Fullname",
                    "dni": "12345678",
                    "phoneNumber": "1234567890",
                    "status": "VERIFICADO",
                },
            ),
            (200, "pong"),
            (
                200,
                {
                    "id": str(post_id),
                    "routeId": str(uuid.uuid4()),
                    "userId": str(user_id),
                    "createdAt": "2023-01-01T00:00:00Z",
                    "expireAt": datetime.now() + timedelta(days=5),
                },
            ),
        ],
    ):
        request_data = {
            "description": "Test Offer",
            "size": "MEDIUM",
            "fragile": False,
            "offer": 99.99,
        }
        response = client.post(
            f"/rf004/posts/{post_id}/offers",
            json=request_data,
            headers={"Authorization": f"Bearer {uuid.uuid4()}"},
        )
        assert response.status_code == 412


def test_create_offer_post_has_expired(mock_requests_factory):
    user_id = uuid.uuid4()
    user_id_2 = uuid.uuid4()
    post_id = uuid.uuid4()

    with mock_requests_factory(
        "get",
        [
            (
                200,
                {
                    "id": str(user_id),
                    "username": "test-user",
                    "email": "testuser@example.com",
                    "fullName": "Test User Fullname",
                    "dni": "12345678",
                    "phoneNumber": "1234567890",
                    "status": "VERIFICADO",
                },
            ),
            (200, "pong"),
            (
                200,
                {
                    "id": str(post_id),
                    "routeId": str(uuid.uuid4()),
                    "userId": str(user_id_2),
                    "createdAt": "2023-01-01T00:00:00Z",
                    "expireAt": datetime.now() - timedelta(days=1),
                },
            ),
        ],
    ):
        request_data = {
            "description": "Test Offer",
            "size": "MEDIUM",
            "fragile": False,
            "offer": 99.99,
        }
        response = client.post(
            f"/rf004/posts/{post_id}/offers",
            json=request_data,
            headers={"Authorization": f"Bearer {uuid.uuid4()}"},
        )
        assert response.status_code == 412


def test_create_offer_slow_response(mock_requests_factory):
    user_id = uuid.uuid4()
    user_id_2 = uuid.uuid4()
    post_id = uuid.uuid4()

    with mock_requests_factory(
        "get",
        [
            (
                200,
                {
                    "id": str(user_id),
                    "username": "test-user",
                    "email": "testuser@example.com",
                    "fullName": "Test User Fullname",
                    "dni": "12345678",
                    "phoneNumber": "1234567890",
                    "status": "VERIFICADO",
                },
            ),
            (200, "pong"),
            (
                200,
                {
                    "id": str(post_id),
                    "routeId": str(uuid.uuid4()),
                    "userId": str(user_id_2),
                    "createdAt": "2023-01-01T00:00:00Z",
                    "expireAt": datetime.now() + timedelta(days=5),
                },
            ),
        ],
        simulate_timeout_per_request=[False, False, True],
    ):
        request_data = {
            "description": "Test Offer",
            "size": "MEDIUM",
            "fragile": False,
            "offer": 99.99,
        }
        response = client.post(
            f"/rf004/posts/{post_id}/offers",
            json=request_data,
            headers={"Authorization": f"Bearer {uuid.uuid4()}"},
        )
        assert response.status_code == 503


def test_create_offer_route_not_found(mock_requests_factory):
    user_id = uuid.uuid4()
    user_id_2 = uuid.uuid4()
    post_id = uuid.uuid4()

    with mock_requests_factory(
        "get",
        [
            (
                200,
                {
                    "id": str(user_id),
                    "username": "test-user",
                    "email": "testuser@example.com",
                    "fullName": "Test User Fullname",
                    "dni": "12345678",
                    "phoneNumber": "1234567890",
                    "status": "VERIFICADO",
                },
            ),
            (200, "pong"),
            (
                200,
                {
                    "id": str(post_id),
                    "routeId": str(uuid.uuid4()),
                    "userId": str(user_id_2),
                    "createdAt": "2023-01-01T00:00:00Z",
                    "expireAt": datetime.now() + timedelta(days=5),
                },
            ),
            (404, {"detail": "Route not found"}),
        ],
    ):
        request_data = {
            "description": "Test Offer",
            "size": "MEDIUM",
            "fragile": False,
            "offer": 99.99,
        }
        response = client.post(
            f"/rf004/posts/{uuid.uuid4()}/offers",
            json=request_data,
            headers={"Authorization": f"Bearer {uuid.uuid4()}"},
        )
        assert response.status_code == 404


def test_create_offer_score_fails_and_offer_is_deleted(mock_requests_factory):
    user_id = uuid.uuid4()
    user_id_2 = uuid.uuid4()
    post_id = uuid.uuid4()
    offer_id = uuid.uuid4()
    created_at = datetime.now()

    with mock_requests_factory(
        "get",
        [
            (
                200,
                {
                    "id": str(user_id),
                    "username": "test-user",
                    "email": "testuser@example.com",
                    "fullName": "Test User Fullname",
                    "dni": "12345678",
                    "phoneNumber": "1234567890",
                    "status": "VERIFICADO",
                },
            ),
            (200, "pong"),
            (
                200,
                {
                    "id": str(post_id),
                    "routeId": str(uuid.uuid4()),
                    "userId": str(user_id_2),
                    "createdAt": "2023-01-01T00:00:00Z",
                    "expireAt": datetime.now() + timedelta(days=5),
                },
            ),
            (
                200,
                {
                    "id": str(uuid.uuid4()),
                    "flightId": "FL123",
                    "sourceAirportCode": "JFK",
                    "sourceCountry": "USA",
                    "destinyAirportCode": "LHR",
                    "destinyCountry": "UK",
                    "bagCost": 50,
                    "plannedStartDate": "2023-10-01T10:00:00Z",
                    "plannedEndDate": "2023-10-01T20:00:00Z",
                    "createdAt": "2023-09-01T00:00:00Z",
                    "updatedAt": "2023-09-01T00:00:00Z",
                },
            ),
        ],
    ):
        with mock_requests_factory(
            "post",
            [
                (
                    201,
                    {
                        "id": offer_id,
                        "userId": user_id,
                        "createdAt": created_at.isoformat(),
                    },
                )
            ],
            simulate_timeout_per_request=[False, True],
        ):
            with mock_requests_factory("delete", [(200, {})]):
                with patch(
                    "src.api.impl.http_client.RequestsHttpClient.delete_offer"
                ) as mock_delete_offer:
                    request_data = {
                        "description": "Test Offer",
                        "size": "MEDIUM",
                        "fragile": False,
                        "offer": 99.99,
                    }
                    response = client.post(
                        f"/rf004/posts/{post_id}/offers",
                        json=request_data,
                        headers={"Authorization": f"Bearer {uuid.uuid4()}"},
                    )
                    assert response.status_code == 503
                    mock_delete_offer.assert_called()


def test_create_offer_success(mock_requests_factory):
    user_id = uuid.uuid4()
    user_id_2 = uuid.uuid4()
    post_id = uuid.uuid4()
    offer_id = uuid.uuid4()
    created_at = datetime.now()

    with mock_requests_factory(
        "get",
        [
            (
                200,
                {
                    "id": str(user_id),
                    "username": "test-user",
                    "email": "testuser@example.com",
                    "fullName": "Test User Fullname",
                    "dni": "12345678",
                    "phoneNumber": "1234567890",
                    "status": "VERIFICADO",
                },
            ),
            (200, "pong"),
            (
                200,
                {
                    "id": str(post_id),
                    "routeId": str(uuid.uuid4()),
                    "userId": str(user_id_2),
                    "createdAt": "2023-01-01T00:00:00Z",
                    "expireAt": datetime.now() + timedelta(days=5),
                },
            ),
            (
                200,
                {
                    "id": str(uuid.uuid4()),
                    "flightId": "FL123",
                    "sourceAirportCode": "JFK",
                    "sourceCountry": "USA",
                    "destinyAirportCode": "LHR",
                    "destinyCountry": "UK",
                    "bagCost": 50,
                    "plannedStartDate": "2023-10-01T10:00:00Z",
                    "plannedEndDate": "2023-10-01T20:00:00Z",
                    "createdAt": "2023-09-01T00:00:00Z",
                    "updatedAt": "2023-09-01T00:00:00Z",
                },
            ),
        ],
    ):
        with mock_requests_factory(
            "post",
            [
                (
                    201,
                    {
                        "id": offer_id,
                        "userId": user_id,
                        "createdAt": created_at.isoformat(),
                    },
                ),
                (
                    201,
                    {
                        "id": str(uuid.uuid4()),
                        "createdAt": datetime.now().isoformat(),
                    },
                ),
            ],
        ):
            with mock_requests_factory("delete", [(200, {})]):
                request_data = {
                    "description": "Test Offer",
                    "size": "MEDIUM",
                    "fragile": False,
                    "offer": 99.99,
                }
                response = client.post(
                    f"/rf004/posts/{post_id}/offers",
                    json=request_data,
                    headers={"Authorization": f"Bearer {uuid.uuid4()}"},
                )
                assert response.status_code == 201
                response_data = response.json()

                assert "data" in response_data
                assert "id" in response_data["data"]
                assert "userId" in response_data["data"]
                assert "postId" in response_data["data"]
                assert "createdAt" in response_data["data"]

                assert response_data["data"]["id"] == str(offer_id)
                assert response_data["data"]["postId"] == str(post_id)
                assert response_data["data"]["userId"] == str(user_id)
                assert response_data["data"]["createdAt"] == created_at.isoformat()
