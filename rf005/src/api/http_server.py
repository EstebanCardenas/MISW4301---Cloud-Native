from typing import Annotated
from uuid import UUID

import httpx
from fastapi import APIRouter, Depends, Header, Path, status

from src.adapters.mappings import info_to_response
from src.assembly import build_post_controller
from src.controllers.post_controller import PostController
from src.exceptions.api_exception import ApiException, ApiExceptionType
from src.models.out.rf005_response import RF005Response

router = APIRouter(prefix="/rf005")


def get_token(authorization: Annotated[str | None, Header()] = None) -> str:
    if not authorization:
        raise ApiException(
            ApiExceptionType.AUTH_TOKEN_MISSING, "Authorization token is missing"
        )
    try:
        token = authorization.split(" ")[1]
        return token
    except ValueError:
        raise ApiException(
            ApiExceptionType.AUTH_TOKEN_MISSING, "Invalid authorization token format"
        )


@router.get("/ping", status_code=status.HTTP_200_OK)
def ping() -> str:
    return "pong"


@router.get("/posts/{id}", response_model=RF005Response, status_code=status.HTTP_200_OK)
def get_post(
    id: UUID = Path(description="Id del post a consultar"),
    controller: PostController = Depends(build_post_controller),
    auth_token: str = Depends(get_token),
) -> RF005Response:
    controller.check_urls()
    post = controller.get_post(id, auth_token)
    route = controller.get_route(post.route_id, auth_token)
    offers = controller.get_offers(post.id, auth_token)
    return info_to_response(post, route, offers)
