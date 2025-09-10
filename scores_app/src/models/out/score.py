from datetime import datetime

from pydantic import UUID4, BaseModel


class ScoreResponse(BaseModel):
    id: UUID4
    offerId: str
    value: float
    createdAt: datetime
