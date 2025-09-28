from datetime import datetime

from src.models.internal.credit_card import Status


class CreditCardStatusResponse:
    def __init__(
        self,
        ruv: str,
        created_at: datetime,
        transaction_identifier: str,
        status: Status,
    ) -> None:
        self.ruv = ruv
        self.created_at = created_at
        self.transaction_identifier = transaction_identifier
        self.status = status
