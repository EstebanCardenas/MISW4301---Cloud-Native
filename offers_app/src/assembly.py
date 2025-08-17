from src.controllers.offer import OfferController
from src.repositories.impl.db_offer_repository import DbOfferRepository

repository = DbOfferRepository()


def build_offer_controller() -> OfferController:
    return OfferController(repository)
