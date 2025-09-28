from datetime import datetime
from uuid import UUID


class CreatedCard:

    def __init__(
        self,
        ruv: str,
        token: str,
        issuer: str,
        transaction_identifier: str,
        created_at: datetime,
    ) -> None:
        self.ruv = ruv
        self.token = token
        self.issuer = issuer
        self.transaction_identifier = transaction_identifier
        self.created_at = created_at
