from enum import Enum

from pydantic import UUID4, BaseModel


class UserStatus(Enum):
    PENDING_VERIFY = "POR_VERIFICAR"
    NOT_VERIFIED = "NO_VERIFICADO"
    VERIFIED = "VERIFICADO"


class User(BaseModel):
    id: UUID4
    username: str
    email: str
    full_name: str
    dni: str
    phone_number: str
    status: UserStatus
