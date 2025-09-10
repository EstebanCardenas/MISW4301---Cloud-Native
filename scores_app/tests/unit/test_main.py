from datetime import datetime, timedelta, timezone
from uuid import UUID

from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker

from src.database.config import Base, get_db, get_engine
from src.main import app

# Create test DB engine (SQLite)
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


def test_read_main():
    response = client.get("/scores/ping")
    assert response.status_code == 200
    assert response.json() == "pong"


def test_create_score():
    response = client.post(
        "/scores",
        json={"offerId": "398", "offerAmount": 1234.23, "bagSize": "SMALL", "bagCost": 100},
    )

    data = response.json()

    assert response.status_code == 201

    assert "id" in data
    assert "createdAt" in data

    # Validate UUID
    try:
        UUID(data["id"])
    except ValueError:
        assert False, f"id is not a valid UUID: {data['id']}"

    # Validate datetime format
    try:
        datetime.fromisoformat(data["createdAt"].replace("Z", "+00:00"))
    except ValueError:
        assert False, f"createdAt is not a valid datetime: {data['createdAt']}"


def test_create_score_offerId_already_exists():
    response = client.post(
        "/scores",
        json={"offerId": "398", "offerAmount": 1234.23, "bagSize": "SMALL", "bagCost": 100},
    )

    assert response.status_code == 201

    response = client.post(
        "/scores",
        json={"offerId": "398", "offerAmount": 1234.23, "bagSize": "SMALL", "bagCost": 100},
    )

    assert response.status_code == 412
    assert response.json() == {"msg": "El offerId ya existe"}


def test_get_score():
    response = client.post(
        "/scores",
        json={"offerId": "398", "offerAmount": 1234.23, "bagSize": "SMALL", "bagCost": 100},
    )

    data = response.json()

    response2 = client.get(
        f"/scores/{data['id']}",
    )

    data2 = response2.json()

    assert response2.status_code == 200
    assert data2["id"] == data["id"]
    assert data2["value"] == 1209.23
    assert "createdAt" in data2

    # Validate UUID
    try:
        UUID(data2["id"])
    except ValueError:
        assert False, f"id is not a valid UUID: {data2['id']}"


def test_get_scores():
    response = client.post(
        "/scores",
        json={"offerId": "398", "offerAmount": 1234.23, "bagSize": "SMALL", "bagCost": 100},
    )

    data = response.json()

    response2 = client.get(
        "/scores",
    )

    data2 = response2.json()

    assert response2.status_code == 200
    assert data2[0]["id"] == data["id"]
    assert data2[0]["offerId"] == "398"
    assert data2[0]["value"] == 1209.23
    assert "createdAt" in data2[0]

    # Validate UUID
    try:
        UUID(data2[0]["id"])
    except ValueError:
        assert False, f"id is not a valid UUID: {data2[0]['id']}"

def test_get_scores_with_filter():
    response1 = client.post(
        "/scores",
        json={"offerId": "398", "offerAmount": 1234.23, "bagSize": "SMALL", "bagCost": 100},
    )
    data1 = response1.json()

    response2 = client.post(
        "/scores",
        json={"offerId": "456", "offerAmount": 1234.23, "bagSize": "SMALL", "bagCost": 100},
    )
    data2 = response2.json()

    response3 = client.get("/scores", params={"flight": "398,456"})

    data3 = response3.json()

    ids = [d["id"] for d in data3]
    assert data1["id"] in ids
    assert data2["id"] in ids

def test_get_scores_count():
    client.post(
        "/scores",
       json={"offerId": "398", "offerAmount": 1234.23, "bagSize": "SMALL", "bagCost": 100},
    )

    response2 = client.get(
        "/scores/count",
    )

    data2 = response2.json()

    assert response2.status_code == 200
    assert data2["count"] == 1


def test_delete_score():
    response = client.post(
        "/scores",
        json={"offerId": "398", "offerAmount": 1234.23, "bagSize": "SMALL", "bagCost": 100},
    )

    data = response.json()

    response2 = client.delete(
        f"/scores/{data['id']}",
    )

    data2 = response2.json()

    assert response2.status_code == 200
    assert data2["msg"] == "la utilidad fue eliminada"


def test_reset_scores():
    client.post(
        "/scores",
        json={"offerId": "398", "offerAmount": 1234.23, "bagSize": "SMALL", "bagCost": 100},
    )

    response2 = client.post(
        "/scores/reset",
    )

    data2 = response2.json()

    assert response2.status_code == 200
    assert data2["msg"] == "Todos los datos fueron eliminados"
