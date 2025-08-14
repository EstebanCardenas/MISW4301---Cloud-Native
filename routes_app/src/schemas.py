from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class RouteBase(BaseModel):
    flightId: str
    sourceAirportCode: str
    sourceCountry: str
    destinyAirportCode: str
    destinyCountry: str
    bagCost: int
    plannedStartDate: datetime
    plannedEndDate: datetime


class RouteCreate(RouteBase):
    pass


class RouteCreatedResponse(BaseModel):
    id: UUID
    createdAt: datetime


class Route(RouteBase):
    id: UUID
    createdAt: datetime
    updatedAt: datetime

    model_config = {"from_attributes": True}
