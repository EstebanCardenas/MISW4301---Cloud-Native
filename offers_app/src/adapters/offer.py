from src.models.incoming.create_offer import CreateOfferRequest
from src.models.internal.offer import Offer
from src.models.out.create_offer import CreateOfferResponse
from src.models.out.offer import OfferResponse


def create_in_to_internal(offer: CreateOfferRequest) -> Offer:
    return Offer(
        post_id=offer.postId,
        user_id=offer.userId,
        description=offer.description,
        size=offer.size,
        fragile=offer.fragile,
        offer=offer.offer,
    )


def create_internal_to_out(offer: Offer) -> CreateOfferResponse:
    return CreateOfferResponse(
        id=offer.id, userId=offer.user_id, createdAt=offer.created_at
    )


def offer_internal_to_out(offer: Offer) -> OfferResponse:
    return OfferResponse(
        id=str(offer.id),
        postId=str(offer.post_id),
        userId=str(offer.user_id),
        description=offer.description,
        size=offer.size,
        fragile=offer.fragile,
        offer=offer.offer,
        createdAt=offer.created_at,
    )
