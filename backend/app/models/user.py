from app.core.database import Base
from sqlalchemy import (
    Column, Integer, String, Boolean, Text, DateTime, SmallInteger,
    ForeignKey, Numeric
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from enum import Enum
from sqlalchemy import Enum as SAEnum

class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    line_uid: Mapped[str] = mapped_column(String, unique=True, nullable=True)
    name: Mapped[str] = mapped_column(String)
    phone: Mapped[str] = mapped_column(String, nullable=True)
    has_ordered: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    orders = relationship("Order", back_populates="user")
