import uuid
from datetime import datetime, timezone
from typing import List

import pytest

from src.api.http_client import HttpClient
from src.models.internal.offer import Offer, OfferSize
from src.models.internal.post import Post
from src.models.internal.route import Airport, Route
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

    def get_offers(self, offer_id, auth_token: str) -> List[Offer]:
        return [
            Offer(
                id=uuid.uuid4(),
                post_id=offer_id,
                user_id=uuid.uuid4(),
                description="Test",
                size=OfferSize.SMALL,
                fragile=False,
                offer=10.0,
                created_at=datetime.now(timezone.utc),
            )
        ]

    def get_route(self, route_id, auth_token: str) -> Route:
        return Route(
            id=route_id,
            flight_id=uuid.uuid4(),
            origin=Airport(airport_code="BOG", country="CO"),
            destiny=Airport(airport_code="MDE", country="CO"),
            bag_cost=15,
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
    assert offers[0].post_id == pid

    rid = uuid.uuid4()
    route = client.get_route(rid, token)
    assert route.id == rid
    assert route.origin.airport_code == "BOG"

    score = client.get_score(uuid.uuid4(), token)
    assert hasattr(score, "country")

    user = client.get_user_info(token)
    assert user.status.name == "VERIFIED"
