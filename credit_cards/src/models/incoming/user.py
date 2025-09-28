from pydantic import UUID4, BaseModel


class GetUserResponse(BaseModel):
    id: UUID4
    username: str
    email: str
    fullName: str
    dni: str
    phoneNumber: str
    status: str
