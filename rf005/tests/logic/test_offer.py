import uuid
from datetime import datetime, timezone

import pytest

from src.models.internal.offer import BaseOffer, Offer, OfferSize


def test_offer_size_enum_values():
    assert OfferSize.SMALL.value == "SMALL"
    assert OfferSize.MEDIUM.value == "MEDIUM"
    assert OfferSize.LARGE.value == "LARGE"


def test_base_offer_creation():
    post_id = uuid.uuid4()
    user_id = uuid.uuid4()
    base = BaseOffer(
        post_id=post_id,
        user_id=user_id,
        description="Caja mediana",
        size=OfferSize.MEDIUM,
        fragile=True,
        offer=42.5,
    )

    assert base.post_id == post_id
    assert base.user_id == user_id
    assert base.description == "Caja mediana"
    assert base.size is OfferSize.MEDIUM
    assert base.fragile is True
    assert base.offer == 42.5


def test_offer_creation_happy_path():
    oid = uuid.uuid4()
    post_id = uuid.uuid4()
    user_id = uuid.uuid4()
    created_at = datetime(2025, 1, 2, 3, 4, 5, tzinfo=timezone.utc)

    offer = Offer(
        id=oid,
        post_id=post_id,
        user_id=user_id,
        description="Paquete grande",
        size=OfferSize.LARGE,
        fragile=False,
        offer=99.99,
        created_at=created_at,
    )

    assert isinstance(offer, BaseOffer)
    assert offer.id == oid
    assert offer.post_id == post_id
    assert offer.user_id == user_id
    assert offer.description == "Paquete grande"
    assert offer.size is OfferSize.LARGE
    assert offer.fragile is False
    assert offer.offer == pytest.approx(99.99)
    assert offer.created_at == created_at
