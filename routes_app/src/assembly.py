from src.controllers.route import RouteController
from src.repositories.impl.db_route_repository import DbRouteRepository

repository = DbRouteRepository()


def build_route_controller() -> RouteController:
    return RouteController(repository)
