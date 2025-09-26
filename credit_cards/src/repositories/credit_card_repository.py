from abc import ABC, abstractmethod
from typing import List, Optional

from sqlalchemy.orm import Session

from src.models.internal.credit_card import CreditCard


class CreditCardRepository(ABC):
    """Credit Card repository interface"""

    @abstractmethod
    def create(self, db: Session, credit_card: CreditCard) -> CreditCard:
        """Create a new credit card"""
        pass

    @abstractmethod
    def get_by_id(self, db: Session, id: str) -> Optional[CreditCard]:
        """Get a credit card by ID"""
        pass

    @abstractmethod
    def get_all(self, db: Session) -> List[CreditCard]:
        """Get all credit cards"""
        pass

    @abstractmethod
    def get_count(self, db: Session) -> int:
        """Get the count of all credit cards"""
        pass

    @abstractmethod
    def update(self, db: Session, credit_card: CreditCard) -> CreditCard:
        """Update an existing credit card"""
        pass

    @abstractmethod
    def delete(self, db: Session, id: str) -> None:
        """Delete a credit card by ID"""
        pass

    @abstractmethod
    def reset(self, db: Session) -> None:
        """Reset the database"""
        pass
