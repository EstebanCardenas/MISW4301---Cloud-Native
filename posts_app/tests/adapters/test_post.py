import uuid
from datetime import datetime

from src.adapters.posts import (
    create_in_to_internal,
    create_internal_to_out,
    post_internal_to_out,
)
from src.models.incoming.create_post_request import CreatePostRequest
from src.models.internal.post import Post


def test_types_create_in_to_internal() -> None:
    input_data = CreatePostRequest(
        routeId=uuid.uuid4(),
        userId=uuid.uuid4(),
        expireAt=datetime.now(),
    )
    internal_post = create_in_to_internal(input_data)
    assert isinstance(internal_post.route_id, uuid.UUID)
    assert isinstance(internal_post.user_id, uuid.UUID)
    assert isinstance(internal_post.expire_at, datetime)


def test_values_create_in_to_internal():
    input_data = CreatePostRequest(
        routeId=uuid.uuid4(),
        userId=uuid.uuid4(),
        expireAt=datetime.now(),
    )
    internal_post = create_in_to_internal(input_data)
    assert internal_post.route_id == input_data.routeId
    assert internal_post.user_id == input_data.userId
    assert internal_post.expire_at == input_data.expireAt


def test_types_create_internal_to_out() -> None:
    internal_data = Post(
        id=uuid.uuid4(),
        route_id=uuid.uuid4(),
        user_id=uuid.uuid4(),
        expire_at=datetime.now(),
        created_at=datetime.now(),
    )
    response = create_internal_to_out(internal_data)
    assert isinstance(response.id, uuid.UUID)
    assert isinstance(response.userId, uuid.UUID)
    assert isinstance(response.createdAt, datetime)


def test_values_create_internal_to_out():
    internal_data = Post(
        id=uuid.uuid4(),
        route_id=uuid.uuid4(),
        user_id=uuid.uuid4(),
        expire_at=datetime.now(),
        created_at=datetime.now(),
    )
    response = create_internal_to_out(internal_data)
    assert response.id == internal_data.id
    assert response.userId == internal_data.user_id
    assert response.createdAt == internal_data.created_at


def test_types_offer_internal_to_out() -> None:
    internal_data = Post(
        id=uuid.uuid4(),
        route_id=uuid.uuid4(),
        user_id=uuid.uuid4(),
        expire_at=datetime.now(),
        created_at=datetime.now(),
    )
    response = post_internal_to_out(internal_data)
    assert isinstance(response.id, uuid.UUID)
    assert isinstance(response.routeId, uuid.UUID)
    assert isinstance(response.userId, uuid.UUID)
    assert isinstance(response.expireAt, datetime)
    assert isinstance(response.createdAt, datetime)


def test_values_offer_internal_to_out():
    internal_data = Post(
        id=uuid.uuid4(),
        route_id=uuid.uuid4(),
        user_id=uuid.uuid4(),
        expire_at=datetime.now(),
        created_at=datetime.now(),
    )
    response = post_internal_to_out(internal_data)
    assert response.id == internal_data.id
    assert response.routeId == internal_data.route_id
    assert response.userId == internal_data.user_id
    assert response.expireAt == internal_data.expire_at
    assert response.createdAt == internal_data.created_at
