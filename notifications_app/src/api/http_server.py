from fastapi import APIRouter, Depends, status

from src.models.incoming.notification_request import NotificationRequest
from src.assembly import build_notification_controller
from src.controllers.notification_controller import NotificationController
from src.models.out.notification_response import NotificationResponse

router = APIRouter(prefix="/notifications")


@router.get("/ping", status_code=status.HTTP_200_OK)
def ping() -> str:
    return "pong"


@router.post("/", response_model=NotificationResponse, status_code=status.HTTP_200_OK)
def post_notification(
    request: NotificationRequest,
    controller: NotificationController = Depends(build_notification_controller),
) -> NotificationResponse:
    response = controller.send_notification(request)
    return NotificationResponse(msg=f"Notification sent: {response.msg}")
