import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from src.database.config import Base


class Route(Base):
    __tablename__ = "route"

    id: Column[UUID] = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    flightId: Column[str] = Column(String, unique=True, nullable=False, index=True)
    sourceAirportCode: Column[str] = Column(String, nullable=False)
    sourceCountry: Column[str] = Column(String, nullable=False)
    destinyAirportCode: Column[str] = Column(String, nullable=False)
    destinyCountry: Column[str] = Column(String, nullable=False)
    bagCost: Column[int] = Column(Integer, nullable=False)
    plannedStartDate: Column[datetime] = Column(DateTime, nullable=False)
    plannedEndDate: Column[datetime] = Column(DateTime, nullable=False)
    createdAt: Column[datetime] = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updatedAt: Column[datetime] = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
