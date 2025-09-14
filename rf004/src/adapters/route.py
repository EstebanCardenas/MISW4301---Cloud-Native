from src.models.incoming.route import RouteInfoResponse
from src.models.internal.route import Route


def get_route_in_to_internal(data: RouteInfoResponse) -> Route:
    return Route(
        id=data.id,
        flight_id=data.flightId,
        source_airport_code=data.sourceAirportCode,
        source_country=data.sourceCountry,
        destiny_airport_code=data.destinyAirportCode,
        destiny_country=data.destinyCountry,
        bag_cost=data.bagCost,
        planned_start_date=data.plannedStartDate,
        planned_end_date=data.plannedEndDate,
        created_at=data.createdAt,
        updated_at=data.updatedAt,
    )
