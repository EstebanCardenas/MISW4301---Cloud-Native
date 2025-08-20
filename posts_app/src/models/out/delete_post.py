from pydantic import BaseModel


class DeletePostResponse(BaseModel):
    msg: str
