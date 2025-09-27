from pydantic import BaseModel


class NotificationRequest(BaseModel):
    template: str
    to: str
    subject: str
    data: dict[str, str]
