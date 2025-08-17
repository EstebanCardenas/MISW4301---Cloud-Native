import uuid

from src.logic.offer_validations import validateOffer
from src.models.internal.offer import Offer, OfferSize


def test_invalid_offer_description():
    offer = Offer(
        post_id=uuid.uuid4(),
        user_id=uuid.uuid4(),
        description="a" * 141,
        size=OfferSize.SMALL,
        fragile=True,
        offer=10.0,
    )
    assert validateOffer(offer) == "Description must be 140 characters or less."


def test_invalid_offer_size():
    offer = Offer(
        post_id=uuid.uuid4(),
        user_id=uuid.uuid4(),
        description="Valid description",
        size="extra_large",
        fragile=True,
        offer=10.0,
    )
    assert validateOffer(offer) == "Invalid offer size."


def test_invalid_offer_price():
    offer = Offer(
        post_id=uuid.uuid4(),
        user_id=uuid.uuid4(),
        description="Valid description",
        size=OfferSize.SMALL,
        fragile=True,
        offer=-10.0,
    )
    assert validateOffer(offer) == "Offer price must be positive."


def test_valid_offer():
    offer = Offer(
        post_id=uuid.uuid4(),
        user_id=uuid.uuid4(),
        description="Valid description",
        size=OfferSize.SMALL,
        fragile=True,
        offer=10.0,
    )
    assert validateOffer(offer) is None
