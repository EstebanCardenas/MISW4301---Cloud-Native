from datetime import datetime, timedelta, timezone
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


def test_create_post():
    user_id = uuid4()
    response = client.post(
        "/posts",
        json={
            "routeId": str(uuid4()),
            "userId": str(user_id),
            "expireAt": (datetime.now(timezone.utc) + timedelta(days=1)).isoformat(),
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


def test_get_posts_count():
    response = client.get("/posts/count")
    assert response.status_code == 200
    response_body = response.json()
    assert "count" in response_body
    assert response_body["count"] == 0

    client.post(
        "/posts",
        json={
            "routeId": str(uuid4()),
            "userId": str(uuid4()),
            "expireAt": (datetime.now(timezone.utc) + timedelta(days=1)).isoformat(),
        },
    )

    response = client.get("/posts/count")
    assert response.status_code == 200
    response_body = response.json()
    assert "count" in response_body
    assert response_body["count"] == 1


def test_get_posts():
    post_1 = {
        "routeId": str(uuid4()),
        "userId": str(uuid4()),
        "expireAt": (datetime.now(timezone.utc) + timedelta(days=1)).isoformat(),
    }

    post_2 = {
        "routeId": str(uuid4()),
        "userId": str(uuid4()),
        "expireAt": (datetime.now(timezone.utc) + timedelta(days=1)).isoformat(),
    }

    post_1_id = client.post("/posts", json=post_1).json()["id"]
    post_2_id = client.post("/posts", json=post_2).json()["id"]
    response = client.get("/posts")
    assert response.status_code == 200
    response_body: list = response.json()
    assert len(response_body) == 2
    post_1_response = next(x for x in response_body if x["id"] == post_1_id)
    post_2_response = next(x for x in response_body if x["id"] == post_2_id)
    assert post_1_response["routeId"] == post_1["routeId"]
    assert post_1_response["userId"] == post_1["userId"]
    assert post_2_response["routeId"] == post_2["routeId"]
    assert post_2_response["userId"] == post_2["userId"]


def test_get_post():
    post = {
        "routeId": str(uuid4()),
        "userId": str(uuid4()),
        "expireAt": (datetime.now(timezone.utc) + timedelta(days=1)).isoformat(),
    }
    post_id = client.post("/posts", json=post).json()["id"]
    response = client.get(f"/posts/{post_id}")
    assert response.status_code == 200
    response_body = response.json()
    assert response_body["id"] == post_id
    assert response_body["routeId"] == post["routeId"]
    assert response_body["userId"] == post["userId"]


def test_delete_post():
    post = {
        "routeId": str(uuid4()),
        "userId": str(uuid4()),
        "expireAt": (datetime.now(timezone.utc) + timedelta(days=1)).isoformat(),
    }
    post_id = client.post("/posts", json=post).json()["id"]
    response = client.delete(f"/posts/{post_id}")
    assert response.status_code == 200
    response = client.get(f"/posts/{post_id}")
    assert response.status_code == 404


def test_reset():
    post_1 = {
        "routeId": str(uuid4()),
        "userId": str(uuid4()),
        "expireAt": (datetime.now(timezone.utc) + timedelta(days=1)).isoformat(),
    }

    post_2 = {
        "routeId": str(uuid4()),
        "userId": str(uuid4()),
        "expireAt": (datetime.now(timezone.utc) + timedelta(days=1)).isoformat(),
    }
    client.post("/posts", json=post_1)
    client.post("/posts", json=post_2)
    posts = client.get("/posts").json()
    assert len(posts) == 2
    client.post("/posts/reset")
    posts = client.get("/posts").json()
    assert len(posts) == 0
