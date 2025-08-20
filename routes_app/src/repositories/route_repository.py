from abc import ABC, abstractmethod
from typing import List, Optional

from sqlalchemy.orm import Session

from src.models.internal.filters import RouteFilter
from src.models.internal.route import Route


class RouteRepository(ABC):
    """Route repository interface"""

    @abstractmethod
    def create(self, db: Session, route: Route) -> Route:
        """Create a new route"""
        pass

    @abstractmethod
    def get_by_id(self, db: Session, id: str) -> Optional[Route]:
        """Get an route by ID"""
        pass

    @abstractmethod
    def get_all(self, db: Session, filters: RouteFilter | None = None) -> List[Route]:
        """Get all routes"""
        pass

    @abstractmethod
    def get_count(self, db: Session) -> int:
        """Get the count of all routes"""
        pass

    @abstractmethod
    def delete(self, db: Session, id: str) -> None:
        """Delete an route by ID"""
        pass

    @abstractmethod
    def reset(self, db: Session) -> None:
        """Reset the database"""
        pass
