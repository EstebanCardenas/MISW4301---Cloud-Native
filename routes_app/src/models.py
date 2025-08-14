import uuid

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from .database import Base


class Route(Base):
    __tablename__ = "route"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    flightId = Column(String, unique=True, nullable=False, index=True)
    sourceAirportCode = Column(String, nullable=False)
    sourceCountry = Column(String, nullable=False)
    destinyAirportCode = Column(String, nullable=False)
    destinyCountry = Column(String, nullable=False)
    bagCost = Column(Integer, nullable=False)
    plannedStartDate = Column(DateTime, nullable=False)
    plannedEndDate = Column(DateTime, nullable=False)
    createdAt = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updatedAt = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
