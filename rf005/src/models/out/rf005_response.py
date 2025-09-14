from datetime import datetime
from enum import Enum
from typing import List

from pydantic import UUID4, BaseModel

from src.models.internal.offer import OfferItem
from src.models.internal.route import Route, RouteItem


class OfferSize(Enum):
    SMALL = "SMALL"
    MEDIUM = "MEDIUM"
    LARGE = "LARGE"


class Offer(BaseModel):
    id: UUID4
    userId: UUID4
    description: str
    size: OfferSize
    fragile: bool
    offer: float
    createdAt: datetime


class RF005Data(BaseModel):
    id: UUID4
    expireAt: datetime
    route: RouteItem
    plannedStartDate: datetime
    plannedEndDate: datetime
    createdAt: datetime
    offers: List[OfferItem]


class RF005Response(BaseModel):
    data: RF005Data
