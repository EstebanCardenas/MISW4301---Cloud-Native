from datetime import datetime

from pydantic import UUID4, BaseModel


class CreateOfferRequest(BaseModel):
    postId: UUID4
    userId: UUID4
    description: str
    size: str
    fragile: bool
    offer: float


class OfferData(BaseModel):
    id: UUID4
    userId: UUID4
    postId: UUID4
    createdAt: datetime


class CreateOfferResponse(BaseModel):
    data: OfferData
    msg: str
