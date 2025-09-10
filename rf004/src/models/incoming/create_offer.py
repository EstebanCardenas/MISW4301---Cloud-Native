from datetime import datetime

from pydantic import UUID4, BaseModel


class CreateOfferResponse(BaseModel):
    id: UUID4
    userId: UUID4
    createdAt: datetime


class CreateOfferRequest(BaseModel):
    description: str
    size: str
    fragile: bool
    offer: float
