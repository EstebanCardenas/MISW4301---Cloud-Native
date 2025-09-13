from datetime import datetime
from uuid import UUID


class Score:

    def __init__(self, id: UUID, created_at: datetime):
        self.id = id
        self.created_at = created_at
