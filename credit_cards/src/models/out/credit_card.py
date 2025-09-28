from datetime import datetime

from pydantic import UUID4, BaseModel


class RegisterCreditCardResponse(BaseModel):
    id: UUID4
    userId: str
    createdAt: datetime


class CreditCardResponse(BaseModel):
    id: UUID4
    userId: str
    token: str
    lastFourDigits: str
    issuer: str
    status: str
    createdAt: datetime
    updatedAt: datetime
