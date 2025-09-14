from datetime import datetime

from pydantic import UUID4, BaseModel


class Post(BaseModel):
    id: UUID4
    route_id: UUID4
    user_id: UUID4
    created_at: datetime
    expire_at: datetime
