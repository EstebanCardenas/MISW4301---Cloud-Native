from src.models.incoming.create_route import CreateRouteRequest
from src.models.internal.route import Route
from src.models.out.create_route import CreateRouteResponse
from src.models.out.route import RouteResponse


def create_in_to_internal(route: CreateRouteRequest) -> Route:
    return Route(
        flightId=route.flightId,
        sourceAirportCode=route.sourceAirportCode,
        sourceCountry=route.sourceCountry,
        destinyAirportCode=route.destinyAirportCode,
        destinyCountry=route.destinyCountry,
        bagCost=route.bagCost,
        plannedStartDate=route.plannedStartDate,
        plannedEndDate=route.plannedEndDate,
    )


def create_internal_to_out(route: Route) -> CreateRouteResponse:
    return CreateRouteResponse(id=route.id, createdAt=route.createdAt)


def route_internal_to_out(route: Route) -> RouteResponse:
    return RouteResponse(
        id=str(route.id),
        flightId=route.flightId,
        sourceAirportCode=route.sourceAirportCode,
        sourceCountry=route.sourceCountry,
        destinyAirportCode=route.destinyAirportCode,
        destinyCountry=route.destinyCountry,
        bagCost=route.bagCost,
        plannedStartDate=route.plannedStartDate,
        plannedEndDate=route.plannedEndDate,
        createdAt=route.createdAt,
        updatedAt=route.updatedAt,
    )
