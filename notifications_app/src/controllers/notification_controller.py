from src.models.incoming.notification_request import NotificationRequest
from src.api.http_client import HttpClient


class NotificationController:
    def __init__(self, http_client: HttpClient):
        self.http_client = http_client

    def send_notification(self, request: NotificationRequest) -> NotificationRequest:
        return self.http_client.send_notification(request)
        