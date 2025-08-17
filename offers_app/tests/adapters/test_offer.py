import uuid
from datetime import datetime

from src.adapters.offer import (
    create_in_to_internal,
    create_internal_to_out,
    offer_internal_to_out,
)
from src.models.incoming.create_offer import CreateOfferRequest
from src.models.internal.offer import Offer, OfferSize


def test_types_create_in_to_internal() -> None:
    input_data = CreateOfferRequest(
        postId=uuid.uuid4(),
        userId=uuid.uuid4(),
        description="Test offer",
        size=OfferSize.SMALL,
        fragile=True,
        offer=10.0,
    )

    internal_offer = create_in_to_internal(input_data)
    assert isinstance(internal_offer.user_id, uuid.UUID)
    assert isinstance(internal_offer.post_id, uuid.UUID)
    assert isinstance(internal_offer.description, str)
    assert isinstance(internal_offer.size, OfferSize)
    assert isinstance(internal_offer.fragile, bool)
    assert isinstance(internal_offer.offer, float)


def test_values_create_in_to_internal():
    input_data = CreateOfferRequest(
        postId=uuid.uuid4(),
        userId=uuid.uuid4(),
        description="Test offer",
        size=OfferSize.SMALL,
        fragile=True,
        offer=10.0,
    )
    internal_offer = create_in_to_internal(input_data)
    assert internal_offer.post_id == input_data.postId
    assert internal_offer.user_id == input_data.userId
    assert internal_offer.description == input_data.description
    assert internal_offer.size == input_data.size
    assert internal_offer.fragile == input_data.fragile
    assert internal_offer.offer == input_data.offer


def test_types_create_internal_to_out() -> None:
    internal_data = Offer(
        id=uuid.uuid4(),
        post_id=uuid.uuid4(),
        user_id=uuid.uuid4(),
        description="Test offer",
        size=OfferSize.SMALL,
        fragile=True,
        offer=10.0,
        created_at=datetime.now(),
    )
    response = create_internal_to_out(internal_data)
    assert isinstance(response.id, uuid.UUID)
    assert isinstance(response.userId, uuid.UUID)
    assert isinstance(response.createdAt, datetime)


def test_values_create_internal_to_out():
    internal_data = Offer(
        id=uuid.uuid4(),
        post_id=uuid.uuid4(),
        user_id=uuid.uuid4(),
        description="Test offer",
        size=OfferSize.SMALL,
        fragile=True,
        offer=10.0,
        created_at=datetime.now(),
    )
    response = create_internal_to_out(internal_data)
    assert response.id == internal_data.id
    assert response.userId == internal_data.user_id
    assert response.createdAt == internal_data.created_at


def test_types_offer_internal_to_out() -> None:
    internal_data = Offer(
        id=uuid.uuid4(),
        post_id=uuid.uuid4(),
        user_id=uuid.uuid4(),
        description="Test offer",
        size=OfferSize.SMALL,
        fragile=True,
        offer=10.0,
        created_at=datetime.now(),
    )
    response = offer_internal_to_out(internal_data)

    assert isinstance(response.id, uuid.UUID)
    assert isinstance(response.postId, uuid.UUID)
    assert isinstance(response.userId, uuid.UUID)
    assert isinstance(response.description, str)
    assert isinstance(response.size, OfferSize)
    assert isinstance(response.fragile, bool)
    assert isinstance(response.offer, float)
    assert isinstance(response.createdAt, datetime)


def test_values_offer_internal_to_out():
    internal_data = Offer(
        id=uuid.uuid4(),
        post_id=uuid.uuid4(),
        user_id=uuid.uuid4(),
        description="Test offer",
        size=OfferSize.SMALL,
        fragile=True,
        offer=10.0,
        created_at=datetime.now(),
    )
    response = offer_internal_to_out(internal_data)
    assert response.id == internal_data.id
    assert response.postId == internal_data.post_id
    assert response.userId == internal_data.user_id
    assert response.description == internal_data.description
    assert response.size == internal_data.size
    assert response.fragile == internal_data.fragile
    assert response.offer == internal_data.offer
    assert response.createdAt == internal_data.created_at
