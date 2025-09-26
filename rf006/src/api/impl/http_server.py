from typing import Annotated

from fastapi import APIRouter, Header, status
from src.exceptions.api_exception import ApiException, ApiExceptionType

router = APIRouter(prefix="/rf006")


def get_token(authorization: Annotated[str | None, Header()] = None) -> str:
    if not authorization:
        raise ApiException(
            ApiExceptionType.AUTH_TOKEN_MISSING, "Authorization token is missing"
        )

    return authorization


@router.get("/ping", status_code=status.HTTP_200_OK)
def ping() -> str:
    return "pong"
