from uuid import UUID

from fastapi import APIRouter, Depends, Path, Query, status

from src.adapters.route import (
    create_in_to_internal,
    create_internal_to_out,
    route_internal_to_out,
)
from src.assembly import build_route_controller
from src.controllers.route import RouteController
from src.database.config import get_db
from src.models.incoming.create_route import CreateRouteRequest
from src.models.internal.filters import RouteFilter
from src.models.out.create_route import CreateRouteResponse
from src.models.out.delete_route import DeleteRouteResponse
from src.models.out.get_route_count import GetRouteCountResponse
from src.models.out.reset import ResetResponse
from src.models.out.route import RouteResponse

router = APIRouter(prefix="/routes")


@router.post(
    "/", response_model=CreateRouteResponse, status_code=status.HTTP_201_CREATED
)
def create_route(
    route: CreateRouteRequest,
    controller: RouteController = Depends(build_route_controller),
    db=Depends(get_db),
) -> CreateRouteResponse:
    new_route = controller.create_route(db, create_in_to_internal(route))

    return create_internal_to_out(new_route)


@router.get(
    "/count", response_model=GetRouteCountResponse, status_code=status.HTTP_200_OK
)
def get_route_count(
    controller: RouteController = Depends(build_route_controller), db=Depends(get_db)
) -> GetRouteCountResponse:
    count = controller.get_count(db)
    return GetRouteCountResponse(count=count)


@router.get("/ping", status_code=status.HTTP_200_OK)
def ping() -> str:
    return "pong"


@router.post("/reset", response_model=ResetResponse, status_code=status.HTTP_200_OK)
def reset(
    controller: RouteController = Depends(build_route_controller), db=Depends(get_db)
) -> ResetResponse:
    controller.reset(db)

    return ResetResponse(msg="Todos los datos fueron eliminados")


@router.get("/", response_model=list[RouteResponse], status_code=status.HTTP_200_OK)
def get_routes(
    flight: str = Query(None, description="Filter routes by flight ID"),
    controller: RouteController = Depends(build_route_controller),
    db=Depends(get_db),
) -> list[RouteResponse]:
    routes = controller.get_routes(db, RouteFilter(flight_id=flight))

    return [route_internal_to_out(route) for route in routes]


@router.get("/{id}", response_model=RouteResponse, status_code=status.HTTP_200_OK)
def get_route(
    id: UUID = Path(description="The ID of the route to retrieve"),
    controller: RouteController = Depends(build_route_controller),
    db=Depends(get_db),
) -> RouteResponse:
    route = controller.get_route(db, id)

    return route_internal_to_out(route)


@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_route(
    id: UUID = Path(description="The ID of the route to delete"),
    controller: RouteController = Depends(build_route_controller),
    db=Depends(get_db),
) -> DeleteRouteResponse:
    controller.delete_route(db, id)

    return DeleteRouteResponse(msg="el trayecto fue eliminado")
