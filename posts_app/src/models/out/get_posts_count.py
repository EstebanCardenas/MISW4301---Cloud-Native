from pydantic import BaseModel


class GetPostsCountResponse(BaseModel):
    count: int
