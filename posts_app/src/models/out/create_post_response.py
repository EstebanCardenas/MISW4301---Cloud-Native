from datetime import datetime

from pydantic import UUID4, BaseModel


class CreatePostResponse(BaseModel):
    id: UUID4
    userId: UUID4
    createdAt: datetime
