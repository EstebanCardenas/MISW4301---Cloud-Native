class RegisterCreditCard:
    def __init__(
        self, card_number: str, cvv: str, expiration_date: str, card_holder_name: str
    ) -> None:
        self.card_number = card_number
        self.cvv = cvv
        self.expiration_date = expiration_date
        self.card_holder_name = card_holder_name
