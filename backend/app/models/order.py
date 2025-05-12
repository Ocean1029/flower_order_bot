from app.core.database import Base
from sqlalchemy import (
    Column, Integer, String, Boolean, Text, DateTime, SmallInteger,
    ForeignKey, Numeric
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from enum import Enum
from sqlalchemy import Enum as SAEnum


class OrderDraftStatus(str, Enum):
    COLLECTING = "collecting"
    ABANDONED = "abandoned"
    COMPLETED = "completed"

class OrderStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"

class OrderDraft(Base):
    __tablename__ = "order_draft"

    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("chat_room.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    status: Mapped[str] = mapped_column(
        SAEnum(OrderDraftStatus, name="order_draft_status", validate_strings=True),
        default=OrderDraftStatus.COLLECTING
    )
    payload_json: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Order(Base):
    __tablename__ = "order"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    draft_id: Mapped[int] = mapped_column(ForeignKey("order_draft.id"))
    status: Mapped[str] = mapped_column(
        SAEnum(OrderStatus, name="order_status", validate_strings=True),
        default=OrderStatus.PENDING
    )
    item_type: Mapped[str] = mapped_column(String)
    product_name: Mapped[str] = mapped_column(Text)
    quantity: Mapped[int] = mapped_column(Integer)
    notes: Mapped[str] = mapped_column(Text, nullable=True)
    card_message: Mapped[str] = mapped_column(Text, nullable=True)
    receipt_address: Mapped[str] = mapped_column(String, nullable=True)
    total_amount: Mapped[float] = mapped_column(Numeric(10, 2))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="orders")
    shipment = relationship("Shipment", back_populates="order", uselist=False)
    payments = relationship("Payment", back_populates="order")