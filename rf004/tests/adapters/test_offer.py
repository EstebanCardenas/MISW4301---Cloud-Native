import uuid
from datetime import datetime, timedelta

from src.adapters.offer import (
    create_offer_in_to_internal_offer,
    create_offer_internal_to_out,
)
from src.models.incoming.create_offer import CreateOfferResponse
from src.models.internal.offer import BaseOffer, OfferSize


def test_types_create_offer_internal_to_out() -> None:
    input_data = BaseOffer(
        post_id=uuid.uuid4(),
        user_id=uuid.uuid4(),
        description="Test description",
        size=OfferSize.MEDIUM,
        fragile=True,
        offer=100.0,
    )

    out_offer = create_offer_internal_to_out(input_data)
    assert isinstance(out_offer.postId, str)
    assert isinstance(out_offer.userId, str)
    assert isinstance(out_offer.description, str)
    assert isinstance(out_offer.size, str)
    assert isinstance(out_offer.fragile, bool)
    assert isinstance(out_offer.offer, float)


def test_values_post_in_to_internal():
    input_data = BaseOffer(
        post_id=uuid.uuid4(),
        user_id=uuid.uuid4(),
        description="Test description",
        size=OfferSize.MEDIUM,
        fragile=True,
        offer=100.0,
    )

    out_offer = create_offer_internal_to_out(input_data)
    assert out_offer.postId == str(input_data.post_id)
    assert out_offer.userId == str(input_data.user_id)
    assert out_offer.description == input_data.description
    assert out_offer.size == input_data.size.value
    assert out_offer.fragile == input_data.fragile
    assert out_offer.offer == input_data.offer


def test_types_create_offer_in_to_internal_offer():
    response = CreateOfferResponse(
        id=uuid.uuid4(), userId=uuid.uuid4(), createdAt=datetime.now()
    )
    base_offer = BaseOffer(
        post_id=uuid.uuid4(),
        user_id=uuid.uuid4(),
        description="Test description",
        size=OfferSize.MEDIUM,
        fragile=True,
        offer=100.0,
    )

    internal_offer = create_offer_in_to_internal_offer(response, base_offer)
    assert isinstance(internal_offer.id, uuid.UUID)
    assert isinstance(internal_offer.post_id, uuid.UUID)
    assert isinstance(internal_offer.user_id, uuid.UUID)
    assert isinstance(internal_offer.description, str)
    assert isinstance(internal_offer.size, OfferSize)
    assert isinstance(internal_offer.fragile, bool)
    assert isinstance(internal_offer.offer, float)


def test_values_create_offer_in_to_internal_offer():
    response = CreateOfferResponse(
        id=uuid.uuid4(), userId=uuid.uuid4(), createdAt=datetime.now()
    )
    base_offer = BaseOffer(
        post_id=uuid.uuid4(),
        user_id=uuid.uuid4(),
        description="Test description",
        size=OfferSize.MEDIUM,
        fragile=True,
        offer=100.0,
    )

    internal_offer = create_offer_in_to_internal_offer(response, base_offer)
    assert internal_offer.id == response.id
    assert internal_offer.post_id == base_offer.post_id
    assert internal_offer.user_id == base_offer.user_id
    assert internal_offer.description == base_offer.description
    assert internal_offer.size == base_offer.size
    assert internal_offer.fragile == base_offer.fragile
    assert internal_offer.offer == base_offer.offer
