from src.api.impl.http_client import RequestsHttpClient
from src.controllers.credit_cards import CreditCardController
from src.controllers.user import UserController
from src.repositories.impl.db_credit_card_repository import DbCreditCardRepository

http_client = RequestsHttpClient()
repository = DbCreditCardRepository()


def build_credit_card_controller() -> CreditCardController:
    return CreditCardController(http_client, repository)


def build_user_controller() -> UserController:
    return UserController(http_client)
