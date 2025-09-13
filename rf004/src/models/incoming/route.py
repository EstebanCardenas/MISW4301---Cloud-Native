from datetime import datetime

from pydantic import UUID4, BaseModel


class RouteInfoResponse(BaseModel):
    id: UUID4
    flightId: str
    sourceAirportCode: str
    sourceCountry: str
    destinyAirportCode: str
    destinyCountry: str
    bagCost: int
    plannedStartDate: datetime
    plannedEndDate: datetime
    createdAt: datetime
    updatedAt: datetime
