from typing import List

from sqlalchemy.orm import Session

from src.exceptions.api_exception import ApiException, ApiExceptionType
from src.logic.route_validations import validateRoute
from src.models.internal.filters import RouteFilter
from src.models.internal.route import Route
from src.repositories.route_repository import RouteRepository


class RouteController:

    def __init__(self, route_repository: RouteRepository):
        self.route_repository = route_repository

    def create_route(self, db: Session, route: Route) -> Route:
        result = validateRoute(db, route)

        if result is not None:
            raise ApiException(type=ApiExceptionType.VALIDATION_FAILED, detail=result)

        return self.route_repository.create(db, route)

    def get_count(self, db: Session) -> int:
        return self.route_repository.get_count(db)

    def get_routes(
        self, db: Session, filters: RouteFilter | None = None
    ) -> List[Route]:
        return self.route_repository.get_all(db, filters)

    def get_route(self, db: Session, id: str) -> Route:
        route = self.route_repository.get_by_id(db, id)

        if not route:
            raise ApiException(
                type=ApiExceptionType.NOT_FOUND, detail="Route not found"
            )

        return route

    def delete_route(self, db: Session, id: str) -> None:
        route = self.route_repository.get_by_id(db, id)

        if not route:
            raise ApiException(
                type=ApiExceptionType.NOT_FOUND, detail="Route not found"
            )

        self.route_repository.delete(db, id)

    def reset(self, db: Session) -> None:
        self.route_repository.reset(db)
