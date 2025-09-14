from pydantic import UUID4, BaseModel


class Airport(BaseModel):
    airport_code: str
    country: str


class Route(BaseModel):
    id: UUID4
    flight_id: str
    origin: Airport
    destiny: Airport
    bag_cost: int


class AirportItem(BaseModel):
    airportCode: str
    country: str


class RouteItem(BaseModel):
    id: UUID4
    flightId: str
    origin: AirportItem
    destiny: AirportItem
    bagCost: int
