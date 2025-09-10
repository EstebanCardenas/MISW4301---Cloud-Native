from src.api.impl.http_client import RequestsHttpClient
from src.controllers.offer import OfferController
from src.controllers.user import UserController

http_client = RequestsHttpClient()


def build_offer_controller() -> OfferController:
    return OfferController(http_client)


def build_user_controller() -> UserController:
    return UserController(http_client)
