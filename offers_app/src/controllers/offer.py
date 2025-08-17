from typing import List

from sqlalchemy.orm import Session

from src.exceptions.api_exception import ApiException, ApiExceptionType
from src.logic.offer_validations import validateOffer
from src.models.internal.filters import OfferFilter
from src.models.internal.offer import Offer
from src.repositories.offer_repository import OfferRepository


class OfferController:

    def __init__(self, offer_repository: OfferRepository):
        self.offer_repository = offer_repository

    def create_offer(self, db: Session, offer: Offer) -> Offer:
        result = validateOffer(offer)

        if result is not None:
            raise ApiException(type=ApiExceptionType.VALIDATION_FAILED, detail=result)

        return self.offer_repository.create(db, offer)

    def get_count(self, db: Session) -> int:
        return self.offer_repository.get_count(db)

    def get_offers(
        self, db: Session, filters: OfferFilter | None = None
    ) -> List[Offer]:
        return self.offer_repository.get_all(db, filters)

    def get_offer(self, db: Session, id: str) -> Offer:
        offer = self.offer_repository.get_by_id(db, id)

        if not offer:
            raise ApiException(
                type=ApiExceptionType.NOT_FOUND, detail="Offer not found"
            )

        return offer

    def delete_offer(self, db: Session, id: str) -> None:
        offer = self.offer_repository.get_by_id(db, id)

        if not offer:
            raise ApiException(
                type=ApiExceptionType.NOT_FOUND, detail="Offer not found"
            )

        self.offer_repository.delete(db, id)

    def reset(self, db: Session) -> None:
        self.offer_repository.reset(db)
