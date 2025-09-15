import uuid
from datetime import datetime, timezone
from typing import List

import pytest

from src.api.http_client import HttpClient
from src.models.internal.offer import Offer, OfferItem, OfferSize
from src.models.internal.post import Post
from src.models.internal.route import Airport, AirportItem, Route, RouteItem
from src.models.internal.score import Score
from src.models.internal.user import User, UserStatus


class DummyHttpClient(HttpClient):
    def get_post(self, post_id, auth_token: str) -> Post:
        now = datetime.now(timezone.utc)
        return Post(
            id=post_id,
            route_id=uuid.uuid4(),
            user_id=uuid.uuid4(),
            created_at=now,
            expire_at=now,
        )

    def get_offers(self, offer_id, auth_token: str) -> List[OfferItem]:
        return [
            OfferItem(
                id=uuid.uuid4(),
                postId=offer_id,
                userId=uuid.uuid4(),
                description="Test",
                size=OfferSize.SMALL,
                fragile=False,
                offer=10.0,
                createdAt=datetime.now(timezone.utc),
            )
        ]

    def get_route(self, route_id, auth_token: str) -> RouteItem:
        return RouteItem(
            id=route_id,
            flightId="35435",
            origin=AirportItem(airportCode="BOG", country="CO"),
            destiny=AirportItem(airportCode="MDE", country="CO"),
            bagCost=15,
        )

    def get_score(self, offer_id, auth_token: str) -> Score:
        s = Score()
        s.country = "CO"
        return s

    def get_user_info(self, auth_token: str) -> User:
        return User(
            id=uuid.uuid4(),
            username="user1",
            email="user1@example.com",
            full_name="User One",
            dni="123",
            phone_number="555",
            status=UserStatus.VERIFIED,
        )

    def check_urls(self):
        return True


def test_http_client_abstract_methods_enforced():
    with pytest.raises(TypeError):
        HttpClient()  # abstract class cannot be instantiated


def test_dummy_http_client_happy_paths():
    client = DummyHttpClient()
    token = "t"
    pid = uuid.uuid4()
    post = client.get_post(pid, token)
    assert post.id == pid
    assert post.created_at.tzinfo is not None

    offers = client.get_offers(pid, token)
    assert len(offers) == 1
    assert offers[0].postId == pid

    rid = uuid.uuid4()
    route = client.get_route(rid, token)
    assert route.id == rid
    assert route.origin.airportCode == "BOG"

    score = client.get_score(uuid.uuid4(), token)
    assert hasattr(score, "country")

    user = client.get_user_info(token)
    assert user.status.name == "VERIFIED"
