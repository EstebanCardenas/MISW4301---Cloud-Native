import os
from enum import Enum

import requests
from pydantic import UUID4

from src.adapters.offer import (
    create_offer_in_to_internal_offer,
    create_offer_internal_to_out,
)
from src.adapters.post import post_in_to_internal
from src.adapters.user import get_user_response_to_internal
from src.api.http_client import HttpClient
from src.exceptions.api_exception import ApiException, ApiExceptionType
from src.models.incoming.create_offer import CreateOfferResponse
from src.models.incoming.posts import GetPostResponse
from src.models.incoming.users import GetUserResponse
from src.models.internal.offer import BaseOffer, Offer
from src.models.internal.post import Post


class Service(Enum):
    POSTS = "posts_service"
    OFFERS = "offers_service"
    USERS = "users_service"


BASE_URLS = {
    Service.POSTS: os.environ.get("POSTS_SERVICE_URL"),
    Service.OFFERS: os.environ.get("OFFERS_SERVICE_URL"),
    Service.USERS: os.environ.get("USERS_SERVICE_URL"),
}


class RequestsHttpClient(HttpClient):
    def get_post(self, post_id: UUID4) -> Post:
        try:
            response = requests.get(
                f"{BASE_URLS[Service.POSTS]}/{post_id}", timeout=(3, 10)
            )

            match response.status_code:
                case 200:
                    return post_in_to_internal(GetPostResponse(**response.json()))

                case 400:
                    raise ApiException(
                        ApiExceptionType.INVALID_INPUT, "ID de publicación inválido"
                    )

                case 404:
                    raise ApiException(
                        ApiExceptionType.NOT_FOUND, "La publicación no existe"
                    )

                case _:
                    raise ApiException(
                        ApiExceptionType.UNKNOWN_ERROR, "Error desconocido"
                    )
        except requests.RequestException:
            raise ApiException(
                ApiExceptionType.SERVICE_UNAVAILABLE,
                "El servicio está temporalmente fuera de servicio.",
            )

    def create_offer(self, data: BaseOffer) -> Offer:
        try:
            response = requests.post(
                f"{BASE_URLS[Service.OFFERS]}/",
                json=create_offer_internal_to_out(data),
                timeout=(3, 10),
            )

            match response.status_code:
                case 201:
                    return create_offer_in_to_internal_offer(
                        CreateOfferResponse(**response.json()), data
                    )

                case 400:
                    raise ApiException(
                        ApiExceptionType.INVALID_INPUT,
                        response.json().get(
                            "detail", "Los datos de la oferta son inválidos"
                        ),
                    )

                case 412:
                    raise ApiException(
                        ApiExceptionType.VALIDATION_FAILED,
                        response.json().get(
                            "detail", "La validación de la oferta falló"
                        ),
                    )

                case _:
                    raise ApiException(
                        ApiExceptionType.UNKNOWN_ERROR, "Error desconocido"
                    )
        except requests.RequestException:
            raise ApiException(
                ApiExceptionType.SERVICE_UNAVAILABLE,
                "El servicio está temporalmente fuera de servicio.",
            )

    def get_user_info(self, auth_token: UUID4):
        try:
            response = requests.get(
                f"{BASE_URLS[Service.USERS]}/users/me",
                headers={"Authorization": f"Bearer {auth_token}"},
                timeout=(3, 10),
            )

            match response.status_code:
                case 200:
                    return get_user_response_to_internal(
                        GetUserResponse(**response.json())
                    )

                case 401:
                    raise ApiException(
                        ApiExceptionType.AUTH_TOKEN_EXPIRED,
                        "El token de autorización ha expirado",
                    )

                case _:
                    raise ApiException(
                        ApiExceptionType.UNKNOWN_ERROR, "Error desconocido"
                    )
        except requests.RequestException:
            raise ApiException(
                ApiExceptionType.SERVICE_UNAVAILABLE,
                "El servicio de usuarios está temporalmente fuera de servicio.",
            )
