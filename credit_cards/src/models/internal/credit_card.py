from src.database.config import Base
from datetime import datetime
import uuid
from enum import Enum
from sqlalchemy import Column, String, DateTime, Enum as SQLEnum, func
from sqlalchemy.dialects.postgresql import UUID


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
    user_id: Column[str] = Column(String, nullable=False)
    last_four_digits: Column[str] = Column(String(4), nullable=False)
    ruv: Column[str] = Column(String, nullable=False)
    issuer: Column[Issuer] = Column(SQLEnum(Issuer), nullable=False)
    status: Column[Status] = Column(SQLEnum(Status), nullable=False)
    created_at: Column[datetime] = Column(DateTime, server_default=func.now())
    updated_at: Column[datetime] = Column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )
