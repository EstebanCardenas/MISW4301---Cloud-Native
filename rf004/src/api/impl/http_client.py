import os
from enum import Enum

import requests
from pydantic import UUID4

from src.adapters.offer import (
    create_offer_in_to_internal_offer,
    create_offer_internal_to_out,
)
from src.adapters.post import post_in_to_internal
from src.adapters.route import get_route_in_to_internal
from src.adapters.score import create_score_in_to_internal
from src.adapters.user import get_user_response_to_internal
from src.api.http_client import HttpClient
from src.exceptions.api_exception import ApiException, ApiExceptionType
from src.models.incoming.create_offer import CreateOfferResponse
from src.models.incoming.posts import GetPostResponse
from src.models.incoming.route import RouteInfoResponse
from src.models.incoming.score import CreateScoreResponse
from src.models.incoming.users import GetUserResponse
from src.models.internal.offer import BaseOffer, Offer, OfferSize
from src.models.internal.post import Post
from src.models.internal.route import Route
from src.models.internal.score import Score
from src.models.out.score import CreateScoreRequest


class Service(Enum):
    POSTS = "posts_service"
    OFFERS = "offers_service"
    USERS = "users_service"
    SCORE = "score_service"
    ROUTES = "routes_service"


BASE_URLS = {
    Service.POSTS: os.getenv("POSTS_SERVICE_URL"),
    Service.OFFERS: os.getenv("OFFERS_SERVICE_URL"),
    Service.USERS: os.getenv("USERS_SERVICE_URL"),
    Service.SCORE: os.getenv("SCORE_SERVICE_URL"),
    Service.ROUTES: os.getenv("ROUTES_SERVICE_URL"),
}


class RequestsHttpClient(HttpClient):
    def get_post(self, post_id: UUID4) -> Post:
        try:
            print(f"{BASE_URLS[Service.POSTS]}/{post_id}")
            response = requests.get(
                f"{BASE_URLS[Service.POSTS]}/{post_id}", timeout=(3, 10)
            )

            print(response)
            print(response.status_code)

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
        except requests.RequestException as e:
            print(e)
            raise ApiException(
                ApiExceptionType.SERVICE_UNAVAILABLE,
                "El servicio está temporalmente fuera de servicio.",
            )

    def create_offer(self, data: BaseOffer) -> Offer:
        try:
            response = requests.post(
                f"{BASE_URLS[Service.OFFERS]}/",
                json=create_offer_internal_to_out(data).model_dump(),
                timeout=(3, 10),
            )

            print(response)

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

    def create_score(
        self, offer_amount: float, offer_size: OfferSize, bag_cost: int, offer_id: UUID4
    ) -> Score:
        try:
            response = requests.post(
                f"{BASE_URLS[Service.SCORE]}/",
                json=CreateScoreRequest(
                    offerAmount=offer_amount,
                    bagSize=offer_size.value,
                    bagCost=bag_cost,
                    offerId=str(offer_id),
                ).model_dump(),
                timeout=(3, 10),
            )

            print(response)

            match response.status_code:
                case 201:
                    score_data = response.json()
                    return create_score_in_to_internal(
                        CreateScoreResponse(**score_data)
                    )

                case 400:
                    raise ApiException(
                        ApiExceptionType.INVALID_INPUT,
                        response.json().get(
                            "detail", "Los datos para crear el score son inválidos"
                        ),
                    )

                case 412:
                    raise ApiException(
                        ApiExceptionType.VALIDATION_FAILED,
                        response.json().get("detail", "La validación del score falló"),
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

    def delete_offer(self, offer_id: UUID4) -> None:
        try:
            response = requests.delete(
                f"{BASE_URLS[Service.OFFERS]}/{offer_id}",
                timeout=(3, 10),
            )

            print(response)

            match response.status_code:
                case 204:
                    return

                case 400:
                    raise ApiException(
                        ApiExceptionType.INVALID_INPUT, "ID de oferta inválido"
                    )

                case 404:
                    raise ApiException(
                        ApiExceptionType.NOT_FOUND, "La oferta no existe"
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

    def get_route_info(self, route_id: UUID4) -> Route:
        try:
            response = requests.get(
                f"{BASE_URLS[Service.ROUTES]}/{route_id}",
                timeout=(3, 10),
            )

            print(response)

            match response.status_code:
                case 200:
                    return get_route_in_to_internal(
                        RouteInfoResponse(**response.json())
                    )

                case 400:
                    raise ApiException(
                        ApiExceptionType.INVALID_INPUT, "ID de ruta inválido"
                    )

                case 404:
                    raise ApiException(ApiExceptionType.NOT_FOUND, "La ruta no existe")

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

    def offers_service_health_check(self) -> bool:
        try:
            response = requests.get(
                f"{BASE_URLS[Service.OFFERS]}/ping",
                timeout=(3, 10),
            )

            print(response)

            match response.status_code:
                case 200:
                    return True

                case _:
                    raise ApiException(
                        ApiExceptionType.SERVICE_UNAVAILABLE,
                        "El servicio está temporalmente fuera de servicio.",
                    )
        except requests.RequestException as e:
            print(e)
            raise ApiException(
                ApiExceptionType.SERVICE_UNAVAILABLE,
                "El servicio está temporalmente fuera de servicio.",
            )
