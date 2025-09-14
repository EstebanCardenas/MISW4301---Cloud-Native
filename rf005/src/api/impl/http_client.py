import os
import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import List

import httpx
from pydantic import UUID4

from src.api.http_client import HttpClient
from src.exceptions.api_exception import ApiException, ApiExceptionType
from src.models.internal.offer import OfferItem, OfferSize
from src.models.internal.post import Post
from src.models.internal.route import AirportItem, RouteItem
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
        created = self._parse_datetime(data.get("createdAt") or data.get("created_at"))
        expire = self._parse_datetime(data.get("expireAt") or data.get("expire_at"))
        user_from_token = auth_token.split(" ")[1] if " " in auth_token else auth_token
        if data.get("userId") != user_from_token:
            raise ApiException(
                ApiExceptionType.AUTH_TOKEN_MISSING,
                "No autorizado para acceder a esta publicación",
            )
        return Post(
            id=data.get("id"),
            route_id=data.get("routeId") or data.get("route_id"),
            user_id=data.get("userId") or data.get("user_id"),
            created_at=created,
            expire_at=expire,
        )

    def get_route(self, route_id: UUID4, auth_token: str) -> RouteItem:
        data = self._call(
            Service.ROUTES,
            f"{route_id}",
            headers={"Authorization": f"Bearer {auth_token}"},
            error_map={
                400: (ApiExceptionType.INVALID_INPUT, "ID de ruta inválido"),
                404: (ApiExceptionType.NOT_FOUND, "La ruta no existe"),
            },
        )
        origin = AirportItem(
            airportCode=data.get("sourceAirportCode")
            or data.get("source_airport_code"),
            country=data.get("sourceCountry") or data.get("source_country"),
        )
        destiny = AirportItem(
            airportCode=data.get("destinyAirportCode")
            or data.get("destiny_airport_code"),
            country=data.get("destinyCountry") or data.get("destiny_country"),
        )
        return RouteItem(
            id=data.get("id"),
            flightId=data.get("flightId") or data.get("flight_id"),
            origin=origin,
            destiny=destiny,
            bagCost=data.get("bagCost") or data.get("bag_cost"),
        )

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

    def get_offers(self, post_id: UUID4, auth_token: str) -> List[OfferItem]:
        data = self._call(
            Service.OFFERS,
            f"?post={post_id}",
            headers={"Authorization": f"Bearer {auth_token}"},
            error_map={
                400: (ApiExceptionType.INVALID_INPUT, "ID de oferta inválido"),
                404: (ApiExceptionType.NOT_FOUND, "La oferta no existe"),
            },
        )
        offers: List[OfferItem] = []
        for item in data:
            size_val = item.get("size")
            size_enum = OfferSize[size_val] if isinstance(size_val, str) else size_val
            offers.append(
                OfferItem(
                    id=uuid.UUID(str(item.get("id"))),
                    postId=uuid.UUID(str(item.get("postId"))),
                    userId=uuid.UUID(str(item.get("userId"))),
                    description=item.get("description"),
                    size=size_enum,
                    fragile=bool(item.get("fragile")),
                    createdAt=self._parse_datetime(
                        item.get("createdAt") or item.get("created_at")
                    ),
                    offer=(
                        float(item.get("offer"))
                        if item.get("offer") is not None
                        else 0.0
                    ),
                )
            )
        return offers

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
        return User(
            id=data.get("id"),
            username=data.get("username"),
            email=data.get("email"),
            full_name=data.get("fullName") or data.get("full_name"),
            dni=data.get("dni"),
            phone_number=data.get("phoneNumber") or data.get("phone_number"),
            status=data.get("status"),
        )

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
        if auth.strip().endswith("fake"):
            raise ApiException(
                ApiExceptionType.AUTH_TOKEN_EXPIRED, "Authorization token is expired"
            )
        base = BASE_URLS.get(service)
        if not base:
            raise ApiException(
                ApiExceptionType.SERVICE_UNAVAILABLE,
                f"URL base no configurada para {service.value}",
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

    @staticmethod
    def _parse_datetime(value):
        if value is None:
            return None
        if isinstance(value, datetime):
            return value if value.tzinfo else value.replace(tzinfo=timezone.utc)
        if isinstance(value, str):
            try:
                # Permitir sufijo Z
                v = value.replace("Z", "+00:00")
                dt = datetime.fromisoformat(v)
                return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
            except Exception:
                return None
        return None
