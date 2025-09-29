import uuid
from datetime import datetime, timedelta
from functools import wraps
from typing import Any, Optional
from unittest.mock import Mock, patch

import pytest
import requests
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker

from src.database.config import Base, get_db, get_engine
from src.main import app
from src.models.internal.credit_card import CreditCard, Issuer, Status

TEST_DATABASE_URL = "sqlite:///./test.db"
test_engine = get_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


# Dependency override
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Apply override
app.dependency_overrides[get_db] = override_get_db


# Create tables in test DB
Base.metadata.create_all(bind=test_engine)

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


@pytest.fixture
def mock_sqs_send():
    """Mock the SQS send_verify_status_message function."""
    with patch("src.controllers.credit_cards.send_verify_status_message") as mock:
        mock.return_value = {
            "MessageId": "12345",
            "ResponseMetadata": {"HTTPStatusCode": 200},
        }
        yield mock


@pytest.fixture
def db_session():
    """Get database session with automatic rollback."""
    db = next(get_db())
    yield db
    db.rollback()  # Always rollback changes after test
    db.close()


@pytest.fixture(autouse=True)
def reset_db():
    """Reset database before each test."""
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)
    yield


user_id_1 = uuid.uuid4()
user_id_2 = uuid.uuid4()


@pytest.fixture
def sample_credit_cards(db_session) -> list[CreditCard]:
    """Create sample credit cards for testing."""
    cards = []
    for i in range(2):
        card = CreditCard(
            token=f"test_token_{i}",
            user_id=user_id_1,  # Use UUID object directly
            last_four_digits=f"123{i}",
            ruv=f"test_ruv_{i}",
            issuer=Issuer.VISA,
            status=Status.POR_VERIFICAR,
        )
        db_session.add(card)
        cards.append(card)

    db_session.commit()
    # Refresh to get database-generated values
    for card in cards:
        db_session.refresh(card)

    return cards


def test_register_credit_card_incomplete_data():
    response = client.post(
        "/credit-cards",
        json={
            "cardNumber": "4111111111111111",
            "cvv": "123",
            "expirationDate": "12/25",
        },
        headers={"Authorization": "Bearer valid_token"},
    )

    assert response.status_code == 400


def test_register_credit_card_expiration_date_wrong_format(mock_requests_factory):
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
        ],
    ):
        response = client.post(
            "/credit-cards",
            json={
                "cardNumber": "4111111111111111",
                "cardHolderName": "John Doe",
                "cvv": "123",
                "expirationDate": "invalid_date_format",
            },
            headers={"Authorization": "Bearer valid_token"},
        )

        assert response.status_code == 400


def test_register_credit_card_expiration_date_invalid_month(mock_requests_factory):
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
        ],
    ):
        response = client.post(
            "/credit-cards",
            json={
                "cardNumber": "4111111111111111",
                "cardHolderName": "John Doe",
                "cvv": "123",
                "expirationDate": "25/13",
            },
            headers={"Authorization": "Bearer valid_token"},
        )

        assert response.status_code == 400


def test_register_credit_card_expiration_date_invalid_year(mock_requests_factory):
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
        ],
    ):
        response = client.post(
            "/credit-cards",
            json={
                "cardNumber": "4111111111111111",
                "cardHolderName": "John Doe",
                "cvv": "123",
                "expirationDate": "100/12",
            },
            headers={"Authorization": "Bearer valid_token"},
        )

        assert response.status_code == 400


def test_register_credit_card_expired_card(mock_requests_factory):
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
        ],
    ):
        response = client.post(
            "/credit-cards",
            json={
                "cardNumber": "4111111111111111",
                "cardHolderName": "John Doe",
                "cvv": "123",
                "expirationDate": "20/12",
            },
            headers={"Authorization": "Bearer valid_token"},
        )

        assert response.status_code == 412


def test_register_credit_card_already_exists(mock_requests_factory):
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
        ],
    ):
        with mock_requests_factory(
            "post",
            [
                (
                    409,
                    {
                        "error": "Credit card already exists",
                        "code": "CREDIT_CARD_ALREADY_EXISTS",
                    },
                )
            ],
        ):
            response = client.post(
                "/credit-cards",
                json={
                    "cardNumber": "4111111111111111",
                    "cardHolderName": "John Doe",
                    "cvv": "123",
                    "expirationDate": "25/12",
                },
                headers={"Authorization": "Bearer valid_token"},
            )

            assert response.status_code == 409


def test_register_credit_card_success(mock_sqs_send, mock_requests_factory):
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
        ],
    ):
        with mock_requests_factory(
            "post",
            [
                (
                    201,
                    {
                        "RUV": "12345",
                        "token": "12345",
                        "issuer": "DINERS CLUB",
                        "transactionIdentifier": str(uuid.uuid4()),
                        "createdAt": "Sat, 27 Sep 2025 19:21:05 GMT",
                    },
                ),
            ],
        ):
            response = client.post(
                "/credit-cards",
                json={
                    "cardNumber": "4111111111111111",
                    "cardHolderName": "John Doe",
                    "cvv": "123",
                    "expirationDate": "25/12",
                },
                headers={"Authorization": "Bearer valid_token"},
            )

            print(response.json())

            assert response.status_code == 201


def test_get_credit_cards_empty(mock_requests_factory):
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
        ],
    ):
        response = client.get(
            "/credit-cards",
            headers={"Authorization": "Bearer valid_token"},
        )

        assert response.status_code == 200
        assert response.json() == []


def test_get_credit_cards_not_from_user(mock_requests_factory):
    with mock_requests_factory(
        "get",
        [
            (
                200,
                {
                    "id": user_id_2,
                    "username": "test-user",
                    "email": "testuser@example.com",
                    "fullName": "Test User Fullname",
                    "dni": "12345678",
                    "phoneNumber": "1234567890",
                    "status": "VERIFICADO",
                },
            ),
            (200, "pong"),
        ],
    ):

        response = client.get(
            "/credit-cards",
            headers={"Authorization": "Bearer valid_token"},
        )

        assert response.status_code == 200
        assert response.json() == []


def test_get_credit_cards_from_user(
    mock_requests_factory, sample_credit_cards: list[CreditCard]
):
    with mock_requests_factory(
        "get",
        [
            (
                200,
                {
                    "id": user_id_1,
                    "username": "test-user",
                    "email": "testuser@example.com",
                    "fullName": "Test User Fullname",
                    "dni": "12345678",
                    "phoneNumber": "1234567890",
                    "status": "VERIFICADO",
                },
            ),
            (
                200,
                {
                    "RUV": "test_ruv_0",
                    "createdAt": "Sat, 27 Sep 2025 19:21:05 GMT",
                    "transactionIdentifier": str(uuid.uuid4()),
                    "status": "APROBADA",
                },
            ),
            (
                200,
                {
                    "RUV": "test_ruv_1",
                    "createdAt": "Sat, 27 Sep 2025 19:21:05 GMT",
                    "transactionIdentifier": str(uuid.uuid4()),
                    "status": "RECHAZADA",
                },
            ),
        ],
    ):

        response = client.get(
            "/credit-cards",
            headers={"Authorization": "Bearer valid_token"},
        )

        assert response.status_code == 200
        assert len(response.json()) == 2


def test_count_credit_cards(mock_requests_factory, db_session, sample_credit_cards):
    response = client.get("/credit-cards/count")

    assert response.status_code == 200
    assert response.json() == {"count": 2}


def test_reset_db(mock_requests_factory, db_session, sample_credit_cards):
    response = client.get("/credit-cards/count")
    assert response.status_code == 200
    assert response.json() == {"count": 2}

    response = client.post("/credit-cards/reset")
    assert response.status_code == 200

    response = client.get("/credit-cards/count")
    assert response.status_code == 200
    assert response.json() == {"count": 0}


def test_update_credit_card_status(
    mock_requests_factory, db_session, sample_credit_cards: list[CreditCard]
):
    with mock_requests_factory(
        "get",
        [
            (
                200,
                {
                    "id": user_id_1,
                    "username": "test-user",
                    "email": "testuser@example.com",
                    "fullName": "Test User Fullname",
                    "dni": "12345678",
                    "phoneNumber": "1234567890",
                    "status": "VERIFICADO",
                },
            ),
            (
                200,
                {
                    "RUV": "test_ruv_0",
                    "createdAt": "Sat, 27 Sep 2025 19:21:05 GMT",
                    "transactionIdentifier": str(uuid.uuid4()),
                    "status": "APROBADA",
                },
            ),
            (
                202,
                {},
            ),
        ],
    ):
        with mock_requests_factory("post", [(200, {})]):
            credit_card_id = sample_credit_cards[0].id

            response = client.put(
                f"/credit-cards/{credit_card_id}/status",
                json={"newStatus": "APROBADA", "userEmail": "testuser@example.com"},
            )

            print(response.json())
            assert response.status_code == 200

            response = client.get(
                "/credit-cards",
                headers={"Authorization": "Bearer valid_token"},
            )

            assert response.status_code == 200
            cards = response.json()
            for card in cards:
                if card["id"] == str(credit_card_id):
                    assert card["status"] == "APROBADA"
                else:
                    assert card["status"] == "POR_VERIFICAR"
