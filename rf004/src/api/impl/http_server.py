import datetime
import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Header, Path, status

from src.adapters.post_offer import create_post_offer_in_to_internal_offer
from src.assembly import build_offer_controller, build_user_controller
from src.controllers.offer import OfferController
from src.controllers.user import UserController
from src.exceptions.api_exception import ApiException, ApiExceptionType
from src.models.incoming.create_offer import CreateOfferRequest
from src.models.out.create_offer import CreateOfferResponse, OfferData

router = APIRouter(prefix="/rf004")


def get_token(authorization: Annotated[str | None, Header()] = None) -> str:
    if not authorization:
        raise ApiException(
            ApiExceptionType.AUTH_TOKEN_MISSING, "Authorization token is missing"
        )

    return authorization


@router.get("/ping", status_code=status.HTTP_200_OK)
def ping() -> str:
    return "pong"


@router.post(
    "/posts/{post_id}/offers",
    response_model=CreateOfferResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_offer(
    offer: CreateOfferRequest,
    post_id: uuid.UUID = Path(description="The ID of the post to create an offer for"),
    auth_token: str = Depends(get_token),
    offer_controller: OfferController = Depends(build_offer_controller),
    user_controller: UserController = Depends(build_user_controller),
) -> CreateOfferResponse:
    print(auth_token)
    user_info = user_controller.get_user_info(auth_token)
    response = offer_controller.create_offer(
        user_info.id,
        post_id,
        create_post_offer_in_to_internal_offer(offer, post_id, user_info.id),
    )

    return CreateOfferResponse(
        data=OfferData(
            id=response.id,
            userId=response.user_id,
            postId=response.post_id,
            createdAt=response.created_at,
        ),
        msg="¡La oferta fue creada exitosamente!",
    )
