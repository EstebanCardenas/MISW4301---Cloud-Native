from pydantic import BaseModel


class RegisterCreditCardRequest(BaseModel):
    cardNumber: str
    cvv: str
    expirationDate: str
    cardHolderName: str


class UpdateCreditCardStatusRequest(BaseModel):
    newStatus: str
    userEmail: str
