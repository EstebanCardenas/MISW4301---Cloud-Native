import uuid

from src.models.incoming.create_offer import CreateOfferRequest
from src.models.internal.offer import BaseOffer, OfferSize


def create_post_offer_in_to_internal_offer(
    in_offer: CreateOfferRequest, post_id: uuid.UUID, user_id: uuid.UUID
) -> BaseOffer:
    return BaseOffer(
        offer=in_offer.offer,
        description=in_offer.description,
        fragile=in_offer.fragile,
        size=OfferSize(in_offer.size),
        post_id=post_id,
        user_id=user_id,
    )
