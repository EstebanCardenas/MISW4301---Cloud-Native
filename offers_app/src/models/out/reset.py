from pydantic import BaseModel


class ResetResponse(BaseModel):
    msg: str
