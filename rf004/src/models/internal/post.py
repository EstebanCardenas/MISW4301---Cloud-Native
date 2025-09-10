from datetime import datetime

from pydantic import UUID4


class Post:
    def __init__(
        self,
        id: UUID4,
        route_id: UUID4,
        user_id: UUID4,
        created_at: datetime,
        expire_at: datetime,
    ):
        self.id = id
        self.route_id = route_id
        self.user_id = user_id
        self.created_at = created_at
        self.expire_at = expire_at
