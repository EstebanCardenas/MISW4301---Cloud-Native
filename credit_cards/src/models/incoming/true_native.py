from datetime import datetime

from pydantic import UUID4, BaseModel


class RegisterCreditCardResponse(BaseModel):
    RUV: str
    token: str
    issuer: str
    transactionIdentifier: str
    createdAt: datetime
