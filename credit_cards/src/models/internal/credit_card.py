import uuid
from datetime import datetime
from enum import Enum

from sqlalchemy import Column, DateTime
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import String, func
from sqlalchemy.dialects.postgresql import UUID

from src.database.config import Base


class Issuer(Enum):
    """Card issuer types"""

    VISA = "VISA"
    MASTERCARD = "MASTERCARD"
    AMERICAN_EXPRESS = "AMERICAN EXPRESS"
    DISCOVER = "DISCOVER"
    DINERS_CLUB = "DINERS CLUB"
    UNKNOWN = "UNKNOWN"


class Status(Enum):
    """Card status types"""

    POR_VERIFICAR = "POR_VERIFICAR"
    RECHAZADA = "RECHAZADA"
    APROBADA = "APROBADA"


class CreditCard(Base):
    __tablename__ = "credit_cards"

    id: Column[UUID] = Column(UUID, primary_key=True, default=uuid.uuid4)
    token: Column[str] = Column(String(256), nullable=False)
    user_id: Column[UUID] = Column(UUID, nullable=False)
    last_four_digits: Column[str] = Column(String(4), nullable=False)
    ruv: Column[str] = Column(String, nullable=False)
    issuer: Column[Issuer] = Column(SQLEnum(Issuer), nullable=False)
    status: Column[Status] = Column(SQLEnum(Status), nullable=False)
    created_at: Column[datetime] = Column(DateTime, server_default=func.now())
    updated_at: Column[datetime] = Column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )
