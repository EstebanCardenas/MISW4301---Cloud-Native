from datetime import datetime
from enum import Enum

from pydantic import UUID4


class OfferSize(Enum):
    """Enum for offer size"""

    SMALL = "SMALL"
    MEDIUM = "MEDIUM"
    LARGE = "LARGE"


class BaseOffer:
    def __init__(
        self,
        post_id: UUID4,
        user_id: UUID4,
        description: str,
        size: OfferSize,
        fragile: bool,
        offer: float,
    ):
        self.post_id = post_id
        self.user_id = user_id
        self.description = description
        self.size = size
        self.fragile = fragile
        self.offer = offer


class Offer(BaseOffer):

    def __init__(
        self,
        id: UUID4,
        post_id: UUID4,
        user_id: UUID4,
        description: str,
        size: OfferSize,
        fragile: bool,
        offer: float,
        created_at: datetime,
    ):
        super().__init__(post_id, user_id, description, size, fragile, offer)
        self.id = id
        self.created_at = created_at
