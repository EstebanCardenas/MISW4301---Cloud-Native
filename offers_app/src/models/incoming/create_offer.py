from pydantic import UUID4, BaseModel

from src.models.internal.offer import OfferSize


class CreateOfferRequest(BaseModel):
    postId: UUID4
    userId: UUID4
    description: str
    size: OfferSize
    fragile: bool
    offer: float
