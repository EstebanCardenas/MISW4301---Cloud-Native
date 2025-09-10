from abc import ABC, abstractmethod
from typing import List, Optional

from sqlalchemy.orm import Session

from src.models.internal.filters import ScoreFilter
from src.models.internal.score import Score


class ScoreRepository(ABC):
    """Score repository interface"""

    @abstractmethod
    def create(self, db: Session, score: Score) -> Score:
        """Create a new score"""
        pass

    @abstractmethod
    def get_by_id(self, db: Session, id: str) -> Optional[Score]:
        """Get a score by ID"""
        pass

    @abstractmethod
    def get_all(self, db: Session, filters: ScoreFilter | None = None) -> List[Score]:
        """Get all scores"""
        pass

    @abstractmethod
    def get_count(self, db: Session) -> int:
        """Get the count of all scores"""
        pass

    @abstractmethod
    def delete(self, db: Session, id: str) -> None:
        """Delete a score by ID"""
        pass

    @abstractmethod
    def reset(self, db: Session) -> None:
        """Reset the database"""
        pass
