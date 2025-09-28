from pydantic import UUID4, BaseModel


class CardInfo(BaseModel):
    cardNumber: str
    cvv: str
    expirationDate: str
    cardHolderName: str


class RegisterCreditCardRequest(BaseModel):
    card: CardInfo
    transactionIdentifier: str
