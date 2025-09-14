import uuid
from datetime import datetime, timedelta

from src.adapters.post import post_in_to_internal
from src.models.incoming.posts import GetPostResponse


def test_types_post_in_to_internal() -> None:
    input_data = GetPostResponse(
        id=uuid.uuid4(),
        routeId=uuid.uuid4(),
        userId=uuid.uuid4(),
        createdAt=datetime.now(),
        expireAt=datetime.now() + timedelta(days=7),
    )

    internal_post = post_in_to_internal(input_data)
    assert isinstance(internal_post.id, uuid.UUID)
    assert isinstance(internal_post.route_id, uuid.UUID)
    assert isinstance(internal_post.user_id, uuid.UUID)
    assert isinstance(internal_post.created_at, datetime)
    assert isinstance(internal_post.expire_at, datetime)


def test_values_post_in_to_internal():
    input_data = GetPostResponse(
        id=uuid.uuid4(),
        routeId=uuid.uuid4(),
        userId=uuid.uuid4(),
        createdAt=datetime.now(),
        expireAt=datetime.now() + timedelta(days=7),
    )
    internal_post = post_in_to_internal(input_data)
    assert internal_post.id == input_data.id
    assert internal_post.route_id == input_data.routeId
    assert internal_post.user_id == input_data.userId
    assert internal_post.created_at == input_data.createdAt
    assert internal_post.expire_at == input_data.expireAt
