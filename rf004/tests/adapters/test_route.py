import uuid
from datetime import datetime, timedelta

from models.incoming.route import RouteInfoResponse
from models.internal.route import Route
from src.adapters.route import get_route_in_to_internal


def test_types_get_route_in_to_internal() -> None:
    input_data = RouteInfoResponse(
        id=uuid.uuid4(),
        flightId=str(uuid.uuid4()),
        sourceAirportCode="SFO",
        sourceCountry="USA",
        destinyAirportCode="JFK",
        destinyCountry="USA",
        bagCost=100,
        plannedStartDate=datetime.now(),
        plannedEndDate=datetime.now() + timedelta(days=7),
        createdAt=datetime.now(),
        updatedAt=datetime.now(),
    )

    internal_route = get_route_in_to_internal(input_data)
    assert isinstance(internal_route.id, uuid.UUID)
    assert isinstance(internal_route.flight_id, str)
    assert isinstance(internal_route.source_airport_code, str)
    assert isinstance(internal_route.source_country, str)
    assert isinstance(internal_route.destiny_airport_code, str)
    assert isinstance(internal_route.destiny_country, str)
    assert isinstance(internal_route.bag_cost, int)
    assert isinstance(internal_route.planned_start_date, datetime)
    assert isinstance(internal_route.planned_end_date, datetime)
    assert isinstance(internal_route.created_at, datetime)
    assert isinstance(internal_route.updated_at, datetime)


def test_values_get_route_in_to_internal():
    input_data = RouteInfoResponse(
        id=uuid.uuid4(),
        flightId=str(uuid.uuid4()),
        sourceAirportCode="SFO",
        sourceCountry="USA",
        destinyAirportCode="JFK",
        destinyCountry="USA",
        bagCost=100,
        plannedStartDate=datetime.now(),
        plannedEndDate=datetime.now() + timedelta(days=7),
        createdAt=datetime.now(),
        updatedAt=datetime.now(),
    )

    internal_route = get_route_in_to_internal(input_data)
    assert internal_route.id == input_data.id
    assert internal_route.flight_id == input_data.flightId
    assert internal_route.source_airport_code == input_data.sourceAirportCode
    assert internal_route.source_country == input_data.sourceCountry
    assert internal_route.destiny_airport_code == input_data.destinyAirportCode
    assert internal_route.destiny_country == input_data.destinyCountry
    assert internal_route.bag_cost == input_data.bagCost
    assert internal_route.planned_start_date == input_data.plannedStartDate
    assert internal_route.planned_end_date == input_data.plannedEndDate
    assert internal_route.created_at == input_data.createdAt
    assert internal_route.updated_at == input_data.updatedAt
