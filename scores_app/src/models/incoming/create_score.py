from enum import Enum

from pydantic import BaseModel


class OfferSize(Enum):
    """Enum for offer size"""

    SMALL = "SMALL"
    MEDIUM = "MEDIUM"
    LARGE = "LARGE"


class CreateScoreRequest(BaseModel):
    offerAmount: float
    bagSize: OfferSize
    bagCost: int
    offerId: str
