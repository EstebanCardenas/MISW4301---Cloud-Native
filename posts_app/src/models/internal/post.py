import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from src.database.config import Base


class Post(Base):
    """Post domain model"""

    __tablename__ = "posts"

    id: Column[UUID] = Column(UUID, primary_key=True, default=uuid.uuid4)
    route_id: Column[UUID] = Column(UUID, nullable=False)
    user_id: Column[UUID] = Column(UUID, nullable=False)
    expire_at: Column[datetime] = Column(DateTime, nullable=False)
    created_at: Column[datetime] = Column(DateTime, server_default=func.now())
