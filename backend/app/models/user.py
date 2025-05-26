from app.core.database import Base
from sqlalchemy import (
    Column, Integer, String, Boolean, Text, DateTime, SmallInteger,
    ForeignKey, Numeric, Enum
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime

class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    line_uid: Mapped[str] = mapped_column(String, unique=True, nullable=True)
    name: Mapped[str] = mapped_column(String)
    phone: Mapped[str] = mapped_column(String, nullable=True)
    avatar_url: Mapped[str] = mapped_column(String, nullable=True)
    has_ordered: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    orders = relationship("Order", foreign_keys="Order.user_id", back_populates="user")
    received_orders = relationship("Order", foreign_keys="Order.receiver_user_id", back_populates="receiver")
    order_drafts = relationship("OrderDraft", foreign_keys="OrderDraft.user_id", back_populates="user")
    received_order_drafts = relationship("OrderDraft", foreign_keys="OrderDraft.receiver_user_id", back_populates="receiver")
