from pydantic import BaseModel


class GetOfferCountResponse(BaseModel):
    count: int
