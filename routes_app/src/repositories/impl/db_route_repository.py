from typing import List, Optional

from sqlalchemy.orm import Session

from src.models.internal.filters import RouteFilter
from src.models.internal.route import Route
from src.repositories.route_repository import RouteRepository


class DbRouteRepository(RouteRepository):
    """Database implementation of the RouteRepository interface"""

    def create(self, db: Session, route: Route) -> Route:
        """Create a new route in the database"""
        db.add(route)
        db.commit()
        db.refresh(route)

        return route

    def get_by_id(self, db: Session, id: str) -> Optional[Route]:
        """Get an route by ID from the database"""
        return db.query(Route).filter(Route.id == id).first()

    def get_all(self, db: Session, filters: RouteFilter | None = None) -> List[Route]:
        """Get all routes from the database"""
        query = db.query(Route)

        if filters:
            if filters.flight_id:
                query = query.filter(Route.flightId == filters.flight_id)

        return query.all()

    def get_count(self, db: Session) -> int:
        """Get the count of all routes in the database"""
        return db.query(Route).count()

    def delete(self, db: Session, id: str) -> None:
        """Delete an route by ID from the database"""
        route = db.query(Route).filter(Route.id == id).first()

        if route:
            db.delete(route)
            db.commit()

    def reset(self, db: Session) -> None:
        """Reset the routes table in the database"""
        db.query(Route).delete()
        db.commit()
