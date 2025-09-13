import os
from enum import Enum
from typing import List

import httpx
from pydantic import UUID4

from src.api.http_client import HttpClient
from src.exceptions.api_exception import ApiException, ApiExceptionType
from src.models.internal.offer import Offer
from src.models.internal.post import Post
from src.models.internal.route import Route
from src.models.internal.score import Score
from src.models.internal.user import User


class Service(Enum):
    POSTS = "posts_service"
    OFFERS = "offers_service"
    ROUTES = "routes_service"
    USERS = "users_service"
    SCORES = "scores_service"


BASE_URLS = {
    Service.POSTS: os.getenv("POSTS_SERVICE_URL"),
    Service.OFFERS: os.getenv("OFFERS_SERVICE_URL"),
    Service.ROUTES: os.getenv("ROUTES_SERVICE_URL"),
    Service.SCORES: os.getenv("SCORES_SERVICE_URL"),
    Service.USERS: os.getenv("USERS_SERVICE_URL"),
}


class RequestsHttpClient(HttpClient):
    def get_post(self, post_id: UUID4, auth_token: str) -> Post:
        data = self._call(
            Service.POSTS,
            f"{post_id}",
            headers={"Authorization": f"Bearer {auth_token}"},
            error_map={
                400: (ApiExceptionType.INVALID_INPUT, "ID de publicación inválido"),
                404: (ApiExceptionType.NOT_FOUND, "La publicación no existe"),
            },
        )
        return Post(**data)

    def get_route(self, route_id: UUID4, auth_token: str) -> Route:
        data = self._call(
            Service.ROUTES,
            f"{route_id}",
            headers={"Authorization": f"Bearer {auth_token}"},
            error_map={
                400: (ApiExceptionType.INVALID_INPUT, "ID de ruta inválido"),
                404: (ApiExceptionType.NOT_FOUND, "La ruta no existe"),
            },
        )
        return Route(**data)

    def get_score(self, offer_id: UUID4, auth_token: str) -> Score:
        data = self._call(
            Service.SCORES,
            f"{offer_id}",
            headers={"Authorization": f"Bearer {auth_token}"},
            error_map={
                400: (ApiExceptionType.INVALID_INPUT, "ID de oferta inválido"),
                404: (ApiExceptionType.NOT_FOUND, "La oferta no existe"),
            },
        )
        return Score(**data)

    def get_offers(self, offer_id: UUID4, auth_token: str) -> List[Offer]:
        data = self._call(
            Service.OFFERS,
            f"{offer_id}",
            headers={"Authorization": f"Bearer {auth_token}"},
            error_map={
                400: (ApiExceptionType.INVALID_INPUT, "ID de oferta inválido"),
                404: (ApiExceptionType.NOT_FOUND, "La oferta no existe"),
            },
        )
        return [Offer(**item) for item in data]

    def get_user_info(self, auth_token: str) -> User:
        data = self._call(
            Service.USERS,
            "/me",
            headers={"Authorization": f"Bearer {auth_token}"},
            error_map={
                401: (
                    ApiExceptionType.AUTH_TOKEN_EXPIRED,
                    "El token de autorización ha expirado",
                ),
            },
        )
        return User(**data)

    def _call(
        self,
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
        base = BASE_URLS.get(service)
        if not base:
            raise ApiException(
                ApiExceptionType.SERVICE_UNAVAILABLE,
                f"URL base no configurada para {service.value}",
            )

        url = f"{base.rstrip('/')}/{path.lstrip('/')}"
        print("consultando url:", url)
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
                f"El servicio {service.value} está temporalmente fuera de servicio.",
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
                "Servicio no disponible temporalmente",
            )
        raise ApiException(ApiExceptionType.UNKNOWN_ERROR, "Error desconocido")
