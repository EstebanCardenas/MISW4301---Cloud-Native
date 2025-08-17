from abc import ABC, abstractmethod
from typing import List, Optional

from sqlalchemy.orm import Session

from src.models.internal.filters import OfferFilter
from src.models.internal.offer import Offer


class OfferRepository(ABC):
    """Offer repository interface"""

    @abstractmethod
    def create(self, db: Session, offer: Offer) -> Offer:
        """Create a new offer"""
        pass

    @abstractmethod
    def get_by_id(self, db: Session, id: str) -> Optional[Offer]:
        """Get an offer by ID"""
        pass

    @abstractmethod
    def get_all(self, db: Session, filters: OfferFilter | None = None) -> List[Offer]:
        """Get all offers"""
        pass

    @abstractmethod
    def get_count(self, db: Session) -> int:
        """Get the count of all offers"""
        pass

    @abstractmethod
    def update(self, db: Session, offer: Offer) -> Offer:
        """Update an existing offer"""
        pass

    @abstractmethod
    def delete(self, db: Session, id: str) -> None:
        """Delete an offer by ID"""
        pass

    @abstractmethod
    def reset(self, db: Session) -> None:
        """Reset the database"""
        pass
