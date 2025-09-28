import os
from datetime import datetime
from enum import Enum

import requests

from src.adapters.credit_cards import create_credit_card_response_to_internal
from src.adapters.users import get_user_response_to_internal
from src.api.http_client import HttpClient
from src.exceptions.api_exception import ApiException, ApiExceptionType
from src.models.incoming.true_native import RegisterCreditCardResponse
from src.models.incoming.user import GetUserResponse
from src.models.internal.created_card import CreatedCard
from src.models.internal.credit_card import Status
from src.models.internal.credit_card_status import CreditCardStatusResponse
from src.models.internal.user import User
from src.models.out.true_native import RegisterCreditCardRequest


class Service(Enum):
    TRUE_NATIVE_SERVICE = "true_native_service"
    USERS = "users"
    NOTIFICATIONS = "notifications"


BASE_URLS = {
    Service.TRUE_NATIVE_SERVICE: os.getenv("TRUE_NATIVE_SERVICE_URL"),
    Service.USERS: os.getenv("USERS_SERVICE_URL"),
    Service.NOTIFICATIONS: os.getenv("NOTIFICATIONS_SERVICE_URL"),
}


class RequestsHttpClient(HttpClient):
    def register_credit_card(self, body: RegisterCreditCardRequest) -> CreatedCard:
        try:
            response = requests.post(
                f"{BASE_URLS[Service.TRUE_NATIVE_SERVICE]}/native/cards",
                headers={
                    "Authorization": f"Bearer {os.getenv('TRUE_NATIVE_SECRET_TOKEN')}"
                },
                json=body.model_dump(),
                timeout=(3, 10),
            )

            match response.status_code:
                case 201:
                    response_body = response.json()
                    return create_credit_card_response_to_internal(
                        RegisterCreditCardResponse(
                            RUV=response_body["RUV"],
                            token=response_body["token"],
                            issuer=response_body["issuer"],
                            transactionIdentifier=response_body[
                                "transactionIdentifier"
                            ],
                            createdAt=datetime.strptime(
                                response_body["createdAt"], "%a, %d %b %Y %H:%M:%S %Z"
                            ),
                        )
                    )

                case 400:
                    raise ApiException(
                        ApiExceptionType.INVALID_INPUT, "La petición es inválida"
                    )

                case 401:
                    raise ApiException(
                        ApiExceptionType.AUTH_TOKEN_INVALID, "No autorizado"
                    )

                case 403:
                    raise ApiException(
                        ApiExceptionType.AUTH_TOKEN_MISSING,
                        "El token de autorización no está incluido en la petición",
                    )

                case 409:
                    raise ApiException(
                        ApiExceptionType.DUPLICATED_RESOURCE,
                        "Ya existe una solicitud de verificación en ejecución para esta tarjeta",
                    )

                case 404:
                    raise ApiException(
                        ApiExceptionType.NOT_FOUND, "La publicación no existe"
                    )

                case _:
                    raise ApiException(
                        ApiExceptionType.UNKNOWN_ERROR, "Error desconocido"
                    )
        except requests.RequestException as e:
            print(e)
            raise ApiException(
                ApiExceptionType.SERVICE_UNAVAILABLE,
                "El servicio está temporalmente fuera de servicio.",
            )

    def get_user_info(self, auth_token: str):
        try:
            response = requests.get(
                f"{BASE_URLS[Service.USERS]}/me",
                headers={"Authorization": f"{auth_token}"},
                timeout=(3, 10),
            )

            print(response)

            match response.status_code:
                case 200:
                    return get_user_response_to_internal(
                        GetUserResponse(**response.json())
                    )

                case 401:
                    raise ApiException(
                        ApiExceptionType.AUTH_TOKEN_INVALID,
                        "El token de autorización ha expirado o es inválido",
                    )

                case _:
                    raise ApiException(
                        ApiExceptionType.UNKNOWN_ERROR, "Error desconocido"
                    )
        except requests.RequestException as e:
            print(e)
            raise ApiException(
                ApiExceptionType.SERVICE_UNAVAILABLE,
                "El servicio está temporalmente fuera de servicio.",
            )

    def send_notification(self, email: str, card_number: str, ruv: str) -> None:
        try:
            response = requests.post(
                f"{BASE_URLS[Service.NOTIFICATIONS]}/notifications",
                json={
                    "template": "rf-006",
                    "to": email,
                    "subject": "RF-006: Resultado inscripción tarjeta",
                    "data": {
                        "numero_tarjeta": card_number,
                        "ruv": ruv,
                    },
                },
                timeout=(3, 10),
            )
            print(response)

            match response.status_code:
                case 200:
                    return

                case 400:
                    raise ApiException(
                        ApiExceptionType.INVALID_INPUT, "La petición es inválida"
                    )

                case 401:
                    raise ApiException(
                        ApiExceptionType.AUTH_TOKEN_INVALID, "No autorizado"
                    )

                case 403:
                    raise ApiException(
                        ApiExceptionType.AUTH_TOKEN_MISSING,
                        "El token de autorización no está incluido en la petición",
                    )

                case 404:
                    raise ApiException(
                        ApiExceptionType.NOT_FOUND, "El usuario no existe"
                    )

                case _:
                    raise ApiException(
                        ApiExceptionType.UNKNOWN_ERROR, "Error desconocido"
                    )
        except requests.RequestException as e:
            print(e)
            raise ApiException(
                ApiExceptionType.SERVICE_UNAVAILABLE,
                "El servicio está temporalmente fuera de servicio.",
            )

    def get_credit_card(self, ruv: str) -> CreditCardStatusResponse | None:
        try:
            response = requests.get(
                f"{BASE_URLS[Service.TRUE_NATIVE_SERVICE]}/native/cards/{ruv}",
                headers={
                    "Authorization": f"Bearer {os.getenv('TRUE_NATIVE_SECRET_TOKEN')}"
                },
                timeout=(3, 10),
            )

            print("EP Response: ", response.json())

            match response.status_code:
                case 200:
                    response_body = response.json()
                    return CreditCardStatusResponse(
                        ruv=response_body["RUV"],
                        created_at=datetime.strptime(
                            response_body["createdAt"], "%a, %d %b %Y %H:%M:%S %Z"
                        ),
                        transaction_identifier=response_body["transactionIdentifier"],
                        status=Status(response_body["status"]),
                    )

                case 202:
                    return None

                case 401:
                    raise ApiException(
                        ApiExceptionType.AUTH_TOKEN_INVALID, "No autorizado"
                    )

                case 403:
                    raise ApiException(
                        ApiExceptionType.AUTH_TOKEN_MISSING,
                        "El token de autorización no está incluido en la petición",
                    )

                case 404:
                    raise ApiException(
                        ApiExceptionType.NOT_FOUND, "La tarjeta no existe"
                    )

                case _:
                    raise ApiException(
                        ApiExceptionType.UNKNOWN_ERROR, "Error desconocido"
                    )
        except requests.RequestException as e:
            print(e)
            raise ApiException(
                ApiExceptionType.SERVICE_UNAVAILABLE,
                "El servicio está temporalmente fuera de servicio.",
            )
