from datetime import datetime

from pydantic import UUID4, BaseModel


class CreateScoreResponse(BaseModel):
    id: UUID4
    createdAt: datetime
