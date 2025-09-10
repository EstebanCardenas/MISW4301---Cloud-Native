from pydantic import BaseModel


class GetScoreCountResponse(BaseModel):
    count: int
