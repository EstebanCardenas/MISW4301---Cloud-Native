from pydantic import BaseModel

from models.internal.offer import OfferSize


class CreateScoreRequest(BaseModel):
    offerAmount: float
    bagSize: str
    bagCost: int
    offerId: str
