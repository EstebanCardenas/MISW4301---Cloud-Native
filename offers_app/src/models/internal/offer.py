import uuid
from datetime import datetime
from enum import Enum

from sqlalchemy import Boolean, Column, DateTime, Float, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.types import Enum as SQLEnum

from src.database.config import Base


class OfferSize(Enum):
    """Enum for offer size"""

    SMALL = "SMALL"
    MEDIUM = "MEDIUM"
    LARGE = "LARGE"


class Offer(Base):
    """Offer domain model"""

    __tablename__ = "offers"

    id: Column[UUID] = Column(UUID, primary_key=True, default=uuid.uuid4)
    post_id: Column[UUID] = Column(UUID, nullable=False)
    user_id: Column[UUID] = Column(UUID, nullable=False)
    description: Column[str] = Column(String(140), nullable=False)
    size: Column[OfferSize] = Column(SQLEnum(OfferSize), nullable=False)
    fragile: Column[bool] = Column(Boolean, default=False)
    offer: Column[float] = Column(Float, nullable=False)
    created_at: Column[datetime] = Column(DateTime, server_default=func.now())
