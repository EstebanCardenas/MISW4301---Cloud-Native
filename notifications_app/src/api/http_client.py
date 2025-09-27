from abc import ABC, abstractmethod


from src.models.incoming.notification_request import NotificationRequest
from src.models.out.notification_response import NotificationResponse


class HttpClient(ABC):
    @abstractmethod
    def send_notification(self, request: NotificationRequest, auth_token: str) -> NotificationResponse:
        pass
