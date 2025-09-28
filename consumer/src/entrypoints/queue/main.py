import json
import logging
import os
import sys

from aws_lambda_powertools.utilities.data_classes import (
    SQSEvent,
    SQSRecord,
    event_source,
)
from config import AppConfig
import httpx
from entrypoints.queue.exceptions.api_exception import (
    ApiException,
    ApiExceptionType,
)
from enum import Enum

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(AppConfig.log_level)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logging.getLogger().setLevel(AppConfig.log_level)
logging.getLogger().addHandler(handler)


def process_record(record: SQSRecord):
    message = record.body
    message_id = record.message_id
    return message, message_id


class Service(Enum):
    CREDIT_CARDS = "credit_cards_service"
    TRUE_NATIVE = "true_native_service"
    TRUE_NATIVE_TOKEN = "true_native_token"
    NOTIFICATIONS = "notifications_service"


BASE_URLS = {
    Service.CREDIT_CARDS: os.getenv("CREDIT_CARDS_URL"),
    Service.TRUE_NATIVE: os.getenv("TRUE_NATIVE_URL"),
    Service.TRUE_NATIVE_TOKEN: os.getenv("SECRET_TOKEN_TRUE_NATIVE"),
    Service.NOTIFICATIONS: os.getenv("NOTIFICATIONS_URL"),
}


# https://docs.powertools.aws.dev/lambda/python/latest/utilities/data_classes/#sqs
@event_source(data_class=SQSEvent)
def handler(event: SQSEvent, context):
    logging.info(f"Received event: {event}")
    # Multiple records can be delivered in a single event
    for record in event.records:
        message, message_id = process_record(record)
        logging.info(f"Raw message: {repr(message)}")
        logging.info(f"Message type: {type(message)}")
        try:
            json_message = json.loads(message)
        except json.JSONDecodeError as e:
            logging.error(f"JSON decode error for message: {repr(message)}")
            logging.error(f"Error details: {e}")
            raise
        logging.info(f"Processed message ID: {message_id}, Body: {json_message}")
        auth_token = BASE_URLS.get(Service.TRUE_NATIVE_TOKEN)
        try:
            response_true_native = _call(
                Service.TRUE_NATIVE,
                f"/cards/{json_message['ruv']}",
                headers={"Authorization": f"Bearer {auth_token}"},
                error_map={
                    401: (
                        ApiExceptionType.AUTH_TOKEN_ERROR,
                        "El secret token no corresponde al definido en el servicio.",
                    ),
                    403: (
                        ApiExceptionType.AUTH_TOKEN_MISSING,
                        "El secret token no corresponde al definido en el servicio.",
                    ),
                    404: (
                        ApiExceptionType.NOT_FOUND,
                        "No existe una verificación en proceso con ese RUV",
                    ),
                    202: (
                        ApiExceptionType.IN_PROCESS_VERIFICATION,
                        "El proceso de registro y verificación aún está en proceso.",
                    ),
                },
            )

            logging.info(f"Success response TrueNative {response_true_native}")

            credit_card_status = _call(
                Service.CREDIT_CARDS,
                f"{json_message['credit_card_id']}/status",
                method="PUT",
                headers={"Authorization": f"Bearer {auth_token}"},
                error_map={
                    404: (
                        ApiExceptionType.NOT_FOUND,
                        "No existe una verificación en proceso con ese RUV",
                    ),
                },
                json={
                    "newStatus": response_true_native["status"],
                    "userEmail": json_message["user_email"],
                },
            )

            logging.info(f"Success response newStatus {credit_card_status}")

        except httpx.RequestError:
            raise ApiException(
                ApiExceptionType.SERVICE_UNAVAILABLE,
                f"El servicio está temporalmente fuera de servicio.",
            )

    return {
        "message": message,
        "message_id": message_id,
    }


def _call(
    service: Service,
    path: str,
    *,
    method: str = "GET",
    json: dict | None = None,
    headers: dict[str, str] | None = None,
    ok_codes: set[int] | None = None,
    error_map: dict[int, tuple[ApiExceptionType, str]] | None = None,
) -> dict:
    auth = headers.get("Authorization") if headers else None
    if not auth:
        raise ApiException(
            ApiExceptionType.AUTH_TOKEN_MISSING, "Authorization token is missing"
        )
    if auth.strip().endswith("fake"):
        raise ApiException(
            ApiExceptionType.AUTH_TOKEN_EXPIRED, "Authorization token is expired"
        )
    base = BASE_URLS.get(service)
    if not base:
        raise ApiException(
            ApiExceptionType.SERVICE_UNAVAILABLE,
            f"Base URL not configured for service {service}",
        )
    url = f"{base.rstrip('/')}/{path.lstrip('/')}"
    try:
        resp = httpx.request(
            method,
            url,
            json=json,
            headers=headers,
            timeout=httpx.Timeout(connect=3.0, read=10.0, write=10.0, pool=3.0),
        )
    except httpx.RequestError:
        raise ApiException(
            ApiExceptionType.SERVICE_UNAVAILABLE,
            f"El servicio está temporalmente fuera de servicio.",
        )

    ok_codes = ok_codes or {200}
    if resp.status_code in ok_codes:
        return resp.json() if resp.content else {}

    # Errores específicos por endpoint (si se proveen)
    if error_map and resp.status_code in error_map:
        ex_type, msg = error_map[resp.status_code]
        raise ApiException(ex_type, msg)

    # Fallback genérico
    if resp.status_code == 400:
        raise ApiException(ApiExceptionType.INVALID_INPUT, "Entrada inválida")
    if resp.status_code == 401:
        raise ApiException(
            ApiExceptionType.AUTH_TOKEN_EXPIRED, "No autorizado / token expirado"
        )
    if resp.status_code == 404:
        raise ApiException(ApiExceptionType.NOT_FOUND, "Recurso no encontrado")
    if resp.status_code >= 500:
        raise ApiException(
            ApiExceptionType.SERVICE_UNAVAILABLE,
            "El servicio está temporalmente fuera de servicio.",
        )
    raise ApiException(ApiExceptionType.UNKNOWN_ERROR, "Error desconocido")
