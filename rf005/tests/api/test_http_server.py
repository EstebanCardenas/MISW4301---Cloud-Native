from datetime import datetime, timedelta, timezone
from uuid import UUID, uuid4

from starlette.testclient import TestClient

from src.assembly import build_post_controller
from src.exceptions.api_exception import ApiException, ApiExceptionType
from src.main import app
from src.models.internal.offer import OfferItem, OfferSize
from src.models.internal.post import Post
from src.models.internal.route import AirportItem, RouteItem


class _FakeController:
    def __init__(self, *, raise_on: str | None = None):
        self.raise_on = raise_on

    def get_post(self, post_id: UUID, auth_token: str) -> Post:
        if self.raise_on == "post":
            raise ApiException(ApiExceptionType.NOT_FOUND, "La publicación no existe")
        now = datetime.now(timezone.utc)
        return Post(
            id=post_id,
            route_id=uuid4(),
            user_id=uuid4(),
            created_at=now,
            expire_at=now + timedelta(days=1),
        )

    def get_route(self, route_id: UUID, auth_token: str) -> RouteItem:
        return RouteItem(
            id=route_id,
            flightId="AV123",
            origin=AirportItem(airportCode="BOG", country="CO"),
            destiny=AirportItem(airportCode="MIA", country="US"),
            bagCost=50,
        )

    def get_offers(self, post_id: UUID, auth_token: str) -> list[OfferItem]:
        return [
            OfferItem(
                id=uuid4(),
                postId=post_id,
                userId=uuid4(),
                description="Test offer",
                size=OfferSize.SMALL,
                fragile=False,
                offer=100.0,
                createdAt=datetime.now(timezone.utc),
            )
        ]


def _override_controller():
    return _FakeController()


def _override_controller_404():
    return _FakeController(raise_on="post")


def test_ping_ok():
    client = TestClient(app)
    r = client.get("/rf005/ping")
    assert r.status_code == 200
    assert r.json() == "pong"


def test_get_post_missing_authorization_header_returns_403():
    client = TestClient(app)
    # Override controller to avoid any external calls
    app.dependency_overrides[build_post_controller] = _override_controller
    try:
        r = client.get(f"/rf005/posts/{uuid4()}")
        assert r.status_code == 403
        body = r.json()
        assert body.get("error_type") == ApiExceptionType.AUTH_TOKEN_MISSING.value
    finally:
        app.dependency_overrides.pop(build_post_controller, None)
