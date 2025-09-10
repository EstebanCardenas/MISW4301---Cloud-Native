from pydantic import BaseModel


class DeleteScoreResponse(BaseModel):
    msg: str
