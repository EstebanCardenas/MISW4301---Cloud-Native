from src.models.internal.offer import Offer, OfferSize


def validateOffer(offer: Offer) -> str | None:
    """Validates the offer data"""
    if len(offer.description) > 140:
        return "Description must be 140 characters or less."

    if offer.size not in [OfferSize.SMALL, OfferSize.MEDIUM, OfferSize.LARGE]:
        return "Invalid offer size."

    if offer.offer < 0:
        return "Offer price must be positive."

    return None
