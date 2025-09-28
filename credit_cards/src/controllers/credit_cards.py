import base64
import uuid
from datetime import datetime
from typing import List

from sqlalchemy.orm import Session

from src.api.http_client import HttpClient
from src.aws.sqs import send_verify_status_message
from src.exceptions.api_exception import ApiException, ApiExceptionType
from src.models.internal.created_card import CreatedCard
from src.models.internal.credit_card import CreditCard, Status
from src.models.internal.filters import CreditCardFilter
from src.models.internal.register_credit_card import RegisterCreditCard
from src.models.out.true_native import CardInfo, RegisterCreditCardRequest
from src.repositories.credit_card_repository import CreditCardRepository


class CreditCardController:

    def __init__(
        self, http_client: HttpClient, credit_card_repository: CreditCardRepository
    ) -> None:
        self.http_client = http_client
        self.credit_card_repository = credit_card_repository

    def __encode_card_number(self, card_number: str) -> str:
        """
        Simple base64 encoding of card number for transaction identifier.
        Same card number will always produce the same encoded result.
        """
        return base64.b64encode(card_number.encode("utf-8")).decode("utf-8")

    def __validate_expiration_date(self, body: RegisterCreditCard) -> None:
        try:
            expiration_year, expiration_month = map(
                int, body.expiration_date.split("/")
            )

            if expiration_month < 1 or expiration_month > 12:
                raise ApiException(
                    ApiExceptionType.INVALID_INPUT,
                    "El mes es inválido",
                )

            if expiration_year < 0 or expiration_year > 99:
                raise ApiException(
                    ApiExceptionType.INVALID_INPUT,
                    "El año es inválido",
                )

            current_year = (
                datetime.now().year % 100
            )  # Get last two digits of current year
            current_month = datetime.now().month
            if (expiration_year < current_year) or (
                expiration_year == current_year and expiration_month < current_month
            ):
                raise ApiException(
                    ApiExceptionType.VALIDATION_FAILED, "La tarjeta ha expirado"
                )
        except ValueError:
            raise ApiException(
                ApiExceptionType.INVALID_INPUT,
                "El formato de la fecha de expiración es inválido",
            )

    def register_credit_card(
        self, db: Session, body: RegisterCreditCard, user_id: uuid.UUID, user_email: str
    ) -> CreditCard:
        self.__validate_expiration_date(body)

        created_card = self.http_client.register_credit_card(
            RegisterCreditCardRequest(
                card=CardInfo(
                    cardHolderName=body.card_holder_name,
                    cardNumber=body.card_number,
                    cvv=body.cvv,
                    expirationDate=body.expiration_date,
                ),
                transactionIdentifier=self.__encode_card_number(body.card_number),
            )
        )

        credit_card = CreditCard(
            token=created_card.token,
            user_id=user_id,
            last_four_digits=body.card_number[-4:],
            ruv=created_card.ruv,
            issuer=created_card.issuer,
            status=Status.POR_VERIFICAR,
        )
        saved_credit_card = self.credit_card_repository.create(db, credit_card)

        send_verify_status_message(
            created_card.ruv, str(saved_credit_card.id), user_email
        )

        return saved_credit_card

    def get_credit_cards(
        self, db: Session, filters: CreditCardFilter | None = None
    ) -> List[CreditCard]:
        credit_cards = self.credit_card_repository.get_all(db, filters)

        credit_cards_with_status: List[CreditCard] = []
        for card in credit_cards:
            updated_card = self.http_client.get_credit_card(card.ruv)
            print("Updated card: ", updated_card)

            credit_cards_with_status.append(
                CreditCard(
                    id=card.id,
                    token=card.token,
                    user_id=card.user_id,
                    last_four_digits=card.last_four_digits,
                    ruv=card.ruv,
                    issuer=card.issuer,
                    status=updated_card.status if updated_card else card.status,
                    created_at=card.created_at,
                    updated_at=card.updated_at,
                )
            )

            print("Credit cards: ", credit_cards_with_status)

        return credit_cards_with_status

    def count_credit_cards(self, db: Session) -> int:
        return self.credit_card_repository.get_count(db)

    def reset_db(self, db: Session) -> None:
        self.credit_card_repository.reset(db)

    def update_credit_card_status(
        self,
        db: Session,
        credit_card_id: uuid.UUID,
        new_status: Status,
        user_email: str,
    ) -> None:
        credit_card = self.credit_card_repository.get_by_id(db, credit_card_id)

        if not credit_card:
            raise ApiException(
                ApiExceptionType.NOT_FOUND, "La tarjeta de crédito no existe"
            )

        credit_card.status = new_status
        self.credit_card_repository.update(db, credit_card)

        self.http_client.send_notification(
            user_email, credit_card.last_four_digits, credit_card.ruv
        )
