import uuid
from datetime import datetime

from src.adapters.mappings import info_to_response
from src.models.internal.post import Post
from src.models.internal.route import Airport, AirportItem, Route, RouteItem


def test_types_info_to_response() -> None:
    post = Post(
        id=uuid.uuid4(),
        route_id=uuid.uuid4(),
        user_id=uuid.uuid4(),
        expire_at=datetime.now(),
        created_at=datetime.now(),
    )
    route = RouteItem(
        id=uuid.uuid4(),
        flightId="4544",
        origin=AirportItem(airportCode="BOG", country="Colombia"),
        destiny=AirportItem(airportCode="MIA", country="USA"),
        bagCost=100,
    )
    offers = []
    internal_post = info_to_response(post, route, offers)
    assert isinstance(internal_post.data.id, uuid.UUID)
    assert isinstance(internal_post.data.route.id, uuid.UUID)
    assert isinstance(internal_post.data.expireAt, datetime)
    assert isinstance(internal_post.data.createdAt, datetime)
    assert isinstance(internal_post.data.offers, list)


def test_values_info_to_response():
    post = Post(
        id=uuid.uuid4(),
        route_id=uuid.uuid4(),
        user_id=uuid.uuid4(),
        expire_at=datetime.now(),
        created_at=datetime.now(),
    )
    route = RouteItem(
        id=uuid.uuid4(),
        flightId="4544",
        origin=AirportItem(airportCode="BOG", country="Colombia"),
        destiny=AirportItem(airportCode="MIA", country="USA"),
        bagCost=100,
    )
    offers = []
    internal_post = info_to_response(post, route, offers)
    assert internal_post.data.route.id == route.id
    assert internal_post.data.id == post.id
    assert internal_post.data.expireAt == post.expire_at
    assert internal_post.data.createdAt == post.created_at
    assert internal_post.data.offers == offers
    assert internal_post.data.route == route
    assert internal_post.data.route.origin.airportCode == route.origin.airportCode
    assert internal_post.data.route.origin.country == route.origin.country
    assert internal_post.data.route.destiny.airportCode == route.destiny.airportCode
    assert internal_post.data.route.destiny.country == route.destiny.country
    assert internal_post.data.route.bagCost == route.bagCost
    assert internal_post.data.route.flightId == route.flightId
