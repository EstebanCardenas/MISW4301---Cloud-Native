from datetime import datetime

from pydantic import UUID4, BaseModel


class CreatePostRequest(BaseModel):
    routeId: UUID4
    userId: UUID4
    expireAt: datetime
