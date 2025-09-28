import uuid


class CreditCardFilter:
    def __init__(self, user_id: uuid.UUID) -> None:
        self.user_id = user_id
