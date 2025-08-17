from pydantic import BaseModel


class DeleteOfferResponse(BaseModel):
    msg: str
