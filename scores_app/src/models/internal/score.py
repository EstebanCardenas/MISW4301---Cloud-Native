import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, Float, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from src.database.config import Base


class Score(Base):
    __tablename__ = "score"

    id: Column[UUID] = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    offerId: Column[str] = Column(String, unique=True, nullable=False, index=True)
    value: Column[float] = Column(Float, nullable=False)
    createdAt: Column[datetime] = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
