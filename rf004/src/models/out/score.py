from pydantic import BaseModel


class CreateScoreRequest(BaseModel):
    offerAmount: float
    bagSize: str
    bagCost: int
    offerId: str
