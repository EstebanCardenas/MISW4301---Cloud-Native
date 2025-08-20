from pydantic import BaseModel


class GetRouteCountResponse(BaseModel):
    count: int
