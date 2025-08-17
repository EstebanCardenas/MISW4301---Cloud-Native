from typing import List, Optional

from sqlalchemy.orm import Session

from src.models.internal.filters import OfferFilter
from src.models.internal.offer import Offer
from src.repositories.offer_repository import OfferRepository


class DbOfferRepository(OfferRepository):
    """Database implementation of the OfferRepository interface"""

    def create(self, db: Session, offer: Offer) -> Offer:
        """Create a new offer in the database"""
        db.add(offer)
        db.commit()
        db.refresh(offer)

        return offer

    def get_by_id(self, db: Session, id: str) -> Optional[Offer]:
        """Get an offer by ID from the database"""
        return db.query(Offer).filter(Offer.id == id).first()

    def get_all(self, db: Session, filters: OfferFilter | None = None) -> List[Offer]:
        """Get all offers from the database"""
        query = db.query(Offer)

        if filters:
            if filters.post_id:
                query = query.filter(Offer.post_id == filters.post_id)
            if filters.user_id:
                query = query.filter(Offer.user_id == filters.user_id)

        return query.all()

    def get_count(self, db: Session) -> int:
        """Get the count of all offers in the database"""
        return db.query(Offer).count()

    def update(self, db: Session, offer: Offer) -> Offer:
        """Update an existing offer in the database"""
        db.merge(offer)
        db.commit()
        db.refresh(offer)

        return offer

    def delete(self, db: Session, id: str) -> None:
        """Delete an offer by ID from the database"""
        offer = db.query(Offer).filter(Offer.id == id).first()

        if offer:
            db.delete(offer)
            db.commit()

    def reset(self, db: Session) -> None:
        """Reset the offers table in the database"""
        db.query(Offer).delete()
        db.commit()
