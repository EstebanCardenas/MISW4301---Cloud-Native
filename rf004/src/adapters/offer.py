from src.models.incoming.create_offer import CreateOfferResponse
from src.models.internal.offer import BaseOffer, Offer
from src.models.out.create_offer import CreateOfferRequest


def create_offer_internal_to_out(data: BaseOffer) -> CreateOfferRequest:
    return CreateOfferRequest(
        postId=data.post_id,
        userId=data.user_id,
        description=data.description,
        size=data.size.value,
        fragile=data.fragile,
        offer=data.offer,
    )


def create_offer_in_to_internal_offer(
    data: CreateOfferResponse, base_offer: BaseOffer
) -> Offer:
    return Offer(
        id=data.id,
        post_id=base_offer.post_id,
        user_id=base_offer.user_id,
        description=base_offer.description,
        size=base_offer.size,
        fragile=base_offer.fragile,
        offer=base_offer.offer,
        created_at=data.createdAt,
    )
