from datetime import datetime

from pydantic import UUID4, BaseModel


class GetPostResponse(BaseModel):
    id: UUID4
    routeId: UUID4
    userId: UUID4
    createdAt: datetime
    expireAt: datetime
