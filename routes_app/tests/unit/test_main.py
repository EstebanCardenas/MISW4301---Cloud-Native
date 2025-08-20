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
    response = client.get("/routes/ping")
    assert response.status_code == 200
    assert response.json() == "pong"


def test_create_route():
    response = client.post(
        "/routes",
        json={
            "flightId": "398",
            "sourceAirportCode": "BOG",
            "sourceCountry": "Colombia",
            "destinyAirportCode": "LGW",
            "destinyCountry": "Inglaterra",
            "bagCost": 158,
            "plannedStartDate": (
                datetime.now(timezone.utc) + timedelta(days=2)
            ).isoformat(),
            "plannedEndDate": (
                datetime.now(timezone.utc) + timedelta(days=9)
            ).isoformat(),
        },
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


def test_create_route_flightId_already_exists():
    response = client.post(
        "/routes",
        json={
            "flightId": "398",
            "sourceAirportCode": "BOG",
            "sourceCountry": "Colombia",
            "destinyAirportCode": "LGW",
            "destinyCountry": "Inglaterra",
            "bagCost": 158,
            "plannedStartDate": (
                datetime.now(timezone.utc) + timedelta(days=2)
            ).isoformat(),
            "plannedEndDate": (
                datetime.now(timezone.utc) + timedelta(days=9)
            ).isoformat(),
        },
    )

    assert response.status_code == 201

    response = client.post(
        "/routes",
        json={
            "flightId": "398",
            "sourceAirportCode": "BOG",
            "sourceCountry": "Colombia",
            "destinyAirportCode": "LGW",
            "destinyCountry": "Inglaterra",
            "bagCost": 158,
            "plannedStartDate": "2025-08-11T22:05:22.564Z",
            "plannedEndDate": "2025-08-19T22:05:22.564Z",
        },
    )

    assert response.status_code == 412
    assert response.json() == {"msg": "El flightId ya existe"}


def test_create_route_start_date_before_today():
    response = client.post(
        "/routes",
        json={
            "flightId": "398",
            "sourceAirportCode": "BOG",
            "sourceCountry": "Colombia",
            "destinyAirportCode": "LGW",
            "destinyCountry": "Inglaterra",
            "bagCost": 158,
            "plannedStartDate": (
                datetime.now(timezone.utc) - timedelta(days=2)
            ).isoformat(),
            "plannedEndDate": (
                datetime.now(timezone.utc) + timedelta(days=7)
            ).isoformat(),
        },
    )

    assert response.status_code == 412
    assert response.json() == {"msg": "Las fechas del trayecto no son válidas"}


def test_create_route_end_date_before_today():
    response = client.post(
        "/routes",
        json={
            "flightId": "398",
            "sourceAirportCode": "BOG",
            "sourceCountry": "Colombia",
            "destinyAirportCode": "LGW",
            "destinyCountry": "Inglaterra",
            "bagCost": 158,
            "plannedStartDate": (
                datetime.now(timezone.utc) + timedelta(days=2)
            ).isoformat(),
            "plannedEndDate": (
                datetime.now(timezone.utc) - timedelta(days=7)
            ).isoformat(),
        },
    )

    assert response.status_code == 412
    assert response.json() == {"msg": "Las fechas del trayecto no son válidas"}


def test_create_route_end_date_before_start_date():
    response = client.post(
        "/routes",
        json={
            "flightId": "398",
            "sourceAirportCode": "BOG",
            "sourceCountry": "Colombia",
            "destinyAirportCode": "LGW",
            "destinyCountry": "Inglaterra",
            "bagCost": 158,
            "plannedStartDate": (
                datetime.now(timezone.utc) + timedelta(days=3)
            ).isoformat(),
            "plannedEndDate": (
                datetime.now(timezone.utc) + timedelta(days=1)
            ).isoformat(),
        },
    )

    assert response.status_code == 412
    assert response.json() == {"msg": "Las fechas del trayecto no son válidas"}


def test_get_route():
    response = client.post(
        "/routes",
        json={
            "flightId": "398",
            "sourceAirportCode": "BOG",
            "sourceCountry": "Colombia",
            "destinyAirportCode": "LGW",
            "destinyCountry": "Inglaterra",
            "bagCost": 158,
            "plannedStartDate": (
                datetime.now(timezone.utc) + timedelta(days=2)
            ).isoformat(),
            "plannedEndDate": (
                datetime.now(timezone.utc) + timedelta(days=9)
            ).isoformat(),
        },
    )

    data = response.json()

    response2 = client.get(
        f"/routes/{data['id']}",
    )

    data2 = response2.json()

    assert response2.status_code == 200
    assert data2["id"] == data["id"]
    assert data2["sourceAirportCode"] == "BOG"
    assert data2["sourceCountry"] == "Colombia"
    assert data2["destinyAirportCode"] == "LGW"
    assert data2["destinyCountry"] == "Inglaterra"
    assert data2["bagCost"] == 158
    assert "plannedStartDate" in data2
    assert "plannedEndDate" in data2

    # Validate UUID
    try:
        UUID(data2["id"])
    except ValueError:
        assert False, f"id is not a valid UUID: {data2['id']}"

    # Validate datetime format
    try:
        datetime.fromisoformat(data2["plannedStartDate"].replace("Z", "+00:00"))
    except ValueError:
        assert (
            False
        ), f"plannedStartDate is not a valid datetime: {data2['plannedStartDate']}"

    try:
        datetime.fromisoformat(data2["plannedEndDate"].replace("Z", "+00:00"))
    except ValueError:
        assert (
            False
        ), f"plannedEndDate is not a valid datetime: {data2['plannedEndDate']}"


def test_get_routes():
    response = client.post(
        "/routes",
        json={
            "flightId": "398",
            "sourceAirportCode": "BOG",
            "sourceCountry": "Colombia",
            "destinyAirportCode": "LGW",
            "destinyCountry": "Inglaterra",
            "bagCost": 158,
            "plannedStartDate": (
                datetime.now(timezone.utc) + timedelta(days=2)
            ).isoformat(),
            "plannedEndDate": (
                datetime.now(timezone.utc) + timedelta(days=9)
            ).isoformat(),
        },
    )

    data = response.json()

    response2 = client.get(
        "/routes",
    )

    data2 = response2.json()

    assert response2.status_code == 200
    assert data2[0]["id"] == data["id"]
    assert data2[0]["sourceAirportCode"] == "BOG"
    assert data2[0]["sourceCountry"] == "Colombia"
    assert data2[0]["destinyAirportCode"] == "LGW"
    assert data2[0]["destinyCountry"] == "Inglaterra"
    assert data2[0]["bagCost"] == 158
    assert "plannedStartDate" in data2[0]
    assert "plannedEndDate" in data2[0]

    # Validate UUID
    try:
        UUID(data2[0]["id"])
    except ValueError:
        assert False, f"id is not a valid UUID: {data2[0]['id']}"

    # Validate datetime format
    try:
        datetime.fromisoformat(data2[0]["plannedStartDate"].replace("Z", "+00:00"))
    except ValueError:
        assert (
            False
        ), f"plannedStartDate is not a valid datetime: {data2[0]['plannedStartDate']}"

    try:
        datetime.fromisoformat(data2[0]["plannedEndDate"].replace("Z", "+00:00"))
    except ValueError:
        assert (
            False
        ), f"plannedEndDate is not a valid datetime: {data2[0]['plannedEndDate']}"


def test_get_routes_with_filter():
    response = client.post(
        "/routes",
        json={
            "flightId": "398",
            "sourceAirportCode": "BOG",
            "sourceCountry": "Colombia",
            "destinyAirportCode": "LGW",
            "destinyCountry": "Inglaterra",
            "bagCost": 158,
            "plannedStartDate": (
                datetime.now(timezone.utc) + timedelta(days=2)
            ).isoformat(),
            "plannedEndDate": (
                datetime.now(timezone.utc) + timedelta(days=9)
            ).isoformat(),
        },
    )

    data = response.json()

    response2 = client.get("/routes", params={"flight": "398"})

    data2 = response2.json()

    assert response2.status_code == 200
    assert data2[0]["id"] == data["id"]
    assert data2[0]["sourceAirportCode"] == "BOG"
    assert data2[0]["sourceCountry"] == "Colombia"
    assert data2[0]["destinyAirportCode"] == "LGW"
    assert data2[0]["destinyCountry"] == "Inglaterra"
    assert data2[0]["bagCost"] == 158
    assert "plannedStartDate" in data2[0]
    assert "plannedEndDate" in data2[0]

    # Validate UUID
    try:
        UUID(data2[0]["id"])
    except ValueError:
        assert False, f"id is not a valid UUID: {data2[0]['id']}"

    # Validate datetime format
    try:
        datetime.fromisoformat(data2[0]["plannedStartDate"].replace("Z", "+00:00"))
    except ValueError:
        assert (
            False
        ), f"plannedStartDate is not a valid datetime: {data2[0]['plannedStartDate']}"

    try:
        datetime.fromisoformat(data2[0]["plannedEndDate"].replace("Z", "+00:00"))
    except ValueError:
        assert (
            False
        ), f"plannedEndDate is not a valid datetime: {data2[0]['plannedEndDate']}"


def test_get_routes_count():
    client.post(
        "/routes",
        json={
            "flightId": "398",
            "sourceAirportCode": "BOG",
            "sourceCountry": "Colombia",
            "destinyAirportCode": "LGW",
            "destinyCountry": "Inglaterra",
            "bagCost": 158,
            "plannedStartDate": (
                datetime.now(timezone.utc) + timedelta(days=2)
            ).isoformat(),
            "plannedEndDate": (
                datetime.now(timezone.utc) + timedelta(days=9)
            ).isoformat(),
        },
    )

    response2 = client.get(
        "/routes/count",
    )

    data2 = response2.json()

    assert response2.status_code == 200
    assert data2["count"] == 1


def test_delete_route():
    response = client.post(
        "/routes",
        json={
            "flightId": "398",
            "sourceAirportCode": "BOG",
            "sourceCountry": "Colombia",
            "destinyAirportCode": "LGW",
            "destinyCountry": "Inglaterra",
            "bagCost": 158,
            "plannedStartDate": (
                datetime.now(timezone.utc) + timedelta(days=2)
            ).isoformat(),
            "plannedEndDate": (
                datetime.now(timezone.utc) + timedelta(days=9)
            ).isoformat(),
        },
    )

    data = response.json()

    response2 = client.delete(
        f"/routes/{data['id']}",
    )

    data2 = response2.json()

    assert response2.status_code == 200
    assert data2["msg"] == "el trayecto fue eliminado"


def test_reset_routes():
    client.post(
        "/routes",
        json={
            "flightId": "398",
            "sourceAirportCode": "BOG",
            "sourceCountry": "Colombia",
            "destinyAirportCode": "LGW",
            "destinyCountry": "Inglaterra",
            "bagCost": 158,
            "plannedStartDate": (
                datetime.now(timezone.utc) + timedelta(days=2)
            ).isoformat(),
            "plannedEndDate": (
                datetime.now(timezone.utc) + timedelta(days=9)
            ).isoformat(),
        },
    )

    response2 = client.post(
        "/routes/reset",
    )

    data2 = response2.json()

    assert response2.status_code == 200
    assert data2["msg"] == "Todos los datos fueron eliminados"
