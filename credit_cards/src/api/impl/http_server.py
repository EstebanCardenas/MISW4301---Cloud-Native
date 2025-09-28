import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Header, status

from src.assembly import build_credit_card_controller, build_user_controller
from src.controllers.credit_cards import CreditCardController
from src.controllers.user import UserController
from src.database.config import get_db
from src.exceptions.api_exception import ApiException, ApiExceptionType
from src.models.incoming.credit_cards import (
    RegisterCreditCardRequest,
    UpdateCreditCardStatusRequest,
)
from src.models.internal.filters import CreditCardFilter
from src.models.internal.register_credit_card import RegisterCreditCard
from src.models.out.credit_card import CreditCardResponse, RegisterCreditCardResponse

router = APIRouter(prefix="/credit-cards")


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
    "",
    response_model=RegisterCreditCardResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_credit_card(
    credit_card: RegisterCreditCardRequest,
    auth_token: str = Depends(get_token),
    controller: CreditCardController = Depends(build_credit_card_controller),
    user_controller: UserController = Depends(build_user_controller),
    db=Depends(get_db),
) -> RegisterCreditCardResponse:
    user_info = user_controller.get_user_info(auth_token)

    result = controller.register_credit_card(
        db,
        RegisterCreditCard(
            card_number=credit_card.cardNumber,
            card_holder_name=credit_card.cardHolderName,
            cvv=credit_card.cvv,
            expiration_date=credit_card.expirationDate,
        ),
        user_info.id,
        user_email=user_info.email,
    )

    return RegisterCreditCardResponse(
        id=str(result.id),
        userId=str(result.user_id),
        createdAt=result.created_at,
    )


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=list[CreditCardResponse],
)
def get_credit_cards(
    auth_token: str = Depends(get_token),
    controller: CreditCardController = Depends(build_credit_card_controller),
    user_controller: UserController = Depends(build_user_controller),
    db=Depends(get_db),
):
    user_info = user_controller.get_user_info(auth_token)

    result = controller.get_credit_cards(db, CreditCardFilter(user_id=user_info.id))

    return map(
        lambda card: CreditCardResponse(
            id=card.id,
            token=card.token,
            userId=str(card.user_id),
            lastFourDigits=card.last_four_digits,
            issuer=card.issuer,
            status=card.status,
            createdAt=card.created_at,
            updatedAt=card.updated_at,
        ),
        result,
    )


@router.get(
    "/count",
    status_code=status.HTTP_200_OK,
)
def count_credit_cards(
    controller: CreditCardController = Depends(build_credit_card_controller),
    db=Depends(get_db),
):
    result = controller.count_credit_cards(db)

    return {"count": result}


@router.post(
    "/reset",
    status_code=status.HTTP_200_OK,
)
def reset_db(
    controller: CreditCardController = Depends(build_credit_card_controller),
    db=Depends(get_db),
):
    controller.reset_db(db)
    return {"msg": "Todos los datos fueron eliminados"}


@router.put(
    "/{credit_card_id}/status",
    status_code=status.HTTP_200_OK,
)
def update_credit_card_status(
    credit_card_id: uuid.UUID,
    body: UpdateCreditCardStatusRequest,
    controller: CreditCardController = Depends(build_credit_card_controller),
    db=Depends(get_db),
):
    controller.update_credit_card_status(
        db, credit_card_id, body.newStatus, body.userEmail
    )
    return {"msg": "Estado de la tarjeta de crédito actualizado"}
