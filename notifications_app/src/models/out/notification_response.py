from pydantic import BaseModel


class NotificationResponse(BaseModel):
    msg: str
