from datetime import datetime
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker

from src.database.config import Base, get_db, get_engine
from src.main import app

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


@pytest.fixture(autouse=True)
def clean_db():
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)


def test_create_offer():
    user_id = uuid4()
    response = client.post(
        "/offers",
        json={
            "postId": str(uuid4()),
            "userId": str(user_id),
            "description": "Test Offer",
            "size": "LARGE",
            "fragile": False,
            "offer": 100.0,
        },
    )
    assert response.status_code == 201

    response_body = response.json()

    assert "id" in response_body
    assert "userId" in response_body
    assert "createdAt" in response_body

    try:
        UUID(response_body["id"])
    except ValueError:
        assert False, f"id is not a valid UUID: {response_body['id']}"

    assert str(user_id) == response_body["userId"]

    try:
        datetime.fromisoformat(response_body["createdAt"].replace("Z", "+00:00"))
    except ValueError:
        assert False, f"createdAt is not a valid datetime: {response_body['createdAt']}"


def test_get_offer_count():
    response = client.get("/offers/count")

    assert response.status_code == 200
    response_body = response.json()
    assert "count" in response_body
    assert response_body["count"] == 0

    client.post(
        "/offers",
        json={
            "postId": str(uuid4()),
            "userId": str(uuid4()),
            "description": "Test Offer",
            "size": "LARGE",
            "fragile": False,
            "offer": 100.0,
        },
    )

    response = client.get("/offers/count")
    assert response.status_code == 200
    response_body = response.json()
    assert "count" in response_body
    assert response_body["count"] == 1


def test_get_offers():
    offer_1 = {
        "postId": str(uuid4()),
        "userId": str(uuid4()),
        "description": "Test Offer",
        "size": "LARGE",
        "fragile": False,
        "offer": 100.0,
    }
    offer_2 = {
        "postId": str(uuid4()),
        "userId": str(uuid4()),
        "description": "Test Offer 2",
        "size": "MEDIUM",
        "fragile": True,
        "offer": 150.0,
    }

    offer_1_id = client.post("/offers", json=offer_1).json()["id"]
    offer_2_id = client.post("/offers", json=offer_2).json()["id"]

    response = client.get("/offers")

    assert response.status_code == 200
    response_body: list = response.json()
    assert len(response_body) == 2

    offer_1_response = next(x for x in response_body if x["id"] == offer_1_id)
    offer_2_response = next(x for x in response_body if x["id"] == offer_2_id)

    assert offer_1_response["postId"] == offer_1["postId"]
    assert offer_1_response["userId"] == offer_1["userId"]
    assert offer_1_response["description"] == offer_1["description"]
    assert offer_1_response["size"] == offer_1["size"]
    assert offer_1_response["fragile"] == offer_1["fragile"]
    assert offer_1_response["offer"] == offer_1["offer"]

    assert offer_2_response["postId"] == offer_2["postId"]
    assert offer_2_response["userId"] == offer_2["userId"]
    assert offer_2_response["description"] == offer_2["description"]
    assert offer_2_response["size"] == offer_2["size"]
    assert offer_2_response["fragile"] == offer_2["fragile"]
    assert offer_2_response["offer"] == offer_2["offer"]


def test_get_offer():
    offer = {
        "postId": str(uuid4()),
        "userId": str(uuid4()),
        "description": "Test Offer",
        "size": "LARGE",
        "fragile": False,
        "offer": 100.0,
    }
    offer_id = client.post("/offers", json=offer).json()["id"]

    response = client.get(f"/offers/{offer_id}")

    assert response.status_code == 200
    response_body = response.json()

    assert response_body["id"] == offer_id
    assert response_body["postId"] == offer["postId"]
    assert response_body["userId"] == offer["userId"]
    assert response_body["description"] == offer["description"]
    assert response_body["size"] == offer["size"]
    assert response_body["fragile"] == offer["fragile"]
    assert response_body["offer"] == offer["offer"]


def test_delete_offer():
    offer = {
        "postId": str(uuid4()),
        "userId": str(uuid4()),
        "description": "Test Offer",
        "size": "LARGE",
        "fragile": False,
        "offer": 100.0,
    }
    offer_id = client.post("/offers", json=offer).json()["id"]

    response = client.delete(f"/offers/{offer_id}")

    assert response.status_code == 200

    response = client.get(f"/offers/{offer_id}")
    assert response.status_code == 404


def test_reset():
    offer_1 = {
        "postId": str(uuid4()),
        "userId": str(uuid4()),
        "description": "Test Offer",
        "size": "LARGE",
        "fragile": False,
        "offer": 100.0,
    }

    offer_2 = {
        "postId": str(uuid4()),
        "userId": str(uuid4()),
        "description": "Test Offer 2",
        "size": "MEDIUM",
        "fragile": True,
        "offer": 150.0,
    }

    client.post("/offers", json=offer_1)
    client.post("/offers", json=offer_2)

    offers = client.get("/offers").json()
    assert len(offers) == 2

    client.post("/offers/reset")

    offers = client.get("/offers").json()
    assert len(offers) == 0
