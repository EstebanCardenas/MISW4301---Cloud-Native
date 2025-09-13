from pydantic import UUID4, BaseModel


class Airport(BaseModel):
    airport_code: str
    country: str


class Route(BaseModel):
    id: UUID4
    flight_id: UUID4
    origin: Airport
    destiny: Airport
    bag_cost: int
