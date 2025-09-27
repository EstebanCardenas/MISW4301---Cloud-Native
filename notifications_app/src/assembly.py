from src.api.impl.http_client import RequestsHttpClient
from src.controllers.notification_controller import NotificationController


def build_notification_controller() -> NotificationController:
    client = RequestsHttpClient()
    return NotificationController(client)
