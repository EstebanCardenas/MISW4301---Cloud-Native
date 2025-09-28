from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from src.models.internal.credit_card import CreditCard
from src.models.internal.filters import CreditCardFilter
from src.repositories.credit_card_repository import CreditCardRepository


class DbCreditCardRepository(CreditCardRepository):
    """Database implementation of the CreditCardRepository interface"""

    def create(self, db: Session, credit_card: CreditCard) -> CreditCard:
        """Create a new credit card in the database"""
        db.add(credit_card)
        db.commit()
        db.refresh(credit_card)

        return credit_card

    def get_by_id(self, db: Session, id: UUID) -> Optional[CreditCard]:
        """Get a credit card by ID from the database"""
        return db.query(CreditCard).filter(CreditCard.id == id).first()

    def get_all(
        self, db: Session, filters: CreditCardFilter | None = None
    ) -> List[CreditCard]:
        """Get all credit cards from the database"""
        query = db.query(CreditCard)

        if filters:
            query = query.filter(CreditCard.user_id == filters.user_id)

        return query.all()

    def get_count(self, db: Session) -> int:
        """Get the count of all credit cards in the database"""
        return db.query(CreditCard).count()

    def update(self, db: Session, credit_card: CreditCard) -> CreditCard:
        """Update an existing credit card in the database"""
        db.merge(credit_card)
        db.commit()
        db.refresh(credit_card)

        return credit_card

    def delete(self, db: Session, id: str) -> None:
        """Delete a credit card by ID from the database"""
        credit_card = db.query(CreditCard).filter(CreditCard.id == id).first()

        if credit_card:
            db.delete(credit_card)
            db.commit()

    def reset(self, db: Session) -> None:
        """Reset the credit cards table in the database"""
        db.query(CreditCard).delete()
        db.commit()
