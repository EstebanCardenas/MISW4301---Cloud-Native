from datetime import datetime

from pydantic import UUID4, BaseModel


class CreateRouteResponse(BaseModel):
    id: UUID4
    createdAt: datetime
