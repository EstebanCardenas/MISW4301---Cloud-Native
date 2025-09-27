import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from src.models.incoming.notification_request import NotificationRequest
from src.models.out.notification_response import NotificationResponse
from src.api.http_client import HttpClient


class RequestsHttpClient(HttpClient):
    def _render_template(self, template_id: str, context: dict) -> str:
        template = self._get_template(template_id)
        for key, value in context.items():
            template = template.replace(f"{{{{ {key} }}}}", str(value))
        return template

    def _get_template(self, template_id: str) -> str:
        template_path = os.path.join(os.path.dirname(__file__), '..', '..', 'templates', f'{template_id}.html')
        try:
            with open(template_path, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            return f"Template no encontrado: '{template_id}'"

    def send_notification(self, request: NotificationRequest) -> NotificationResponse:
        if not os.getenv('SENDGRID_API_KEY') or not os.getenv('SENDGRID_FROM_EMAIL'):
            return NotificationResponse(msg="Error: SENDGRID_API_KEY o SENDGRID_FROM_EMAIL no estan definidas")

        message = Mail(
            from_email=os.getenv('SENDGRID_FROM_EMAIL'),
            to_emails=request.to,
            subject=request.subject,
            html_content=self._render_template(request.template, request.data)
        )
        try:
            sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
            response = sg.send(message)
            return NotificationResponse(msg="Notificacion enviada")
        except Exception as e:
            return NotificationResponse(msg=f"Error enviando mail: {str(e)}")
    
