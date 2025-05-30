from app.core.database import Base
from sqlalchemy import (
    Column, Integer, String, Boolean, Text, DateTime, SmallInteger,
    ForeignKey, Numeric
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime, timezone, timedelta
from app.enums.order import OrderStatus
from app.enums.shipment import ShipmentMethod, ShipmentStatus
from sqlalchemy import Enum as SAEnum


class OrderDraft(Base):
    __tablename__ = "order_draft"

    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("chat_room.id"))
    
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    receiver_user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=True)
    
    item_type: Mapped[str] = mapped_column(String, nullable=True)
    quantity: Mapped[int] = mapped_column(Integer, nullable=True)
    total_amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=True)
    notes: Mapped[str] = mapped_column(Text, nullable=True)
    card_message: Mapped[str] = mapped_column(Text, nullable=True)
    shipment_method: Mapped[str] = mapped_column(
        SAEnum(ShipmentMethod, name="shipment_method", validate_strings=True),
        default=ShipmentMethod.STORE_PICKUP,
        nullable=True
    )
    shipment_status: Mapped[str] = mapped_column(
        SAEnum(ShipmentStatus, name="shipment_status", validate_strings=True),
        default=ShipmentStatus.PENDING,
        nullable=True
    )
    receipt_address: Mapped[str] = mapped_column(String, nullable=True)
    delivery_address: Mapped[str] = mapped_column(Text, nullable=True)
    delivery_datetime: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone(timedelta(hours=8))).replace(tzinfo=None))
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone(timedelta(hours=8))).replace(tzinfo=None), onupdate=datetime.now(timezone(timedelta(hours=8))).replace(tzinfo=None))

    user = relationship("User", foreign_keys=[user_id], back_populates="order_drafts")
    receiver = relationship("User", foreign_keys=[receiver_user_id], back_populates="received_order_drafts")
    room = relationship("ChatRoom", back_populates="order_drafts")

class Order(Base):
    __tablename__ = "order"

    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("chat_room.id"))
    
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    receiver_user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    
    status: Mapped[str] = mapped_column(
        SAEnum(OrderStatus, name="order_status", validate_strings=True),
        default=OrderStatus.PENDING
    )
    item_type: Mapped[str] = mapped_column(String)
    quantity: Mapped[int] = mapped_column(Integer)
    total_amount: Mapped[float] = mapped_column(Numeric(10, 2))
    notes: Mapped[str] = mapped_column(Text, nullable=True)
    card_message: Mapped[str] = mapped_column(Text, nullable=True)
    shipment_method: Mapped[str] = mapped_column(
        SAEnum(ShipmentMethod, name="shipment_method", validate_strings=True),
        default=ShipmentMethod.STORE_PICKUP
    )
    shipment_status: Mapped[str] = mapped_column(
        SAEnum(ShipmentStatus, name="shipment_status", validate_strings=True),
        default=ShipmentStatus.PENDING
    )
    receipt_address: Mapped[str] = mapped_column(String, nullable=True)
    delivery_address: Mapped[str] = mapped_column(Text, nullable=True)
    delivery_datetime: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone(timedelta(hours=8))).replace(tzinfo=None))
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone(timedelta(hours=8))).replace(tzinfo=None), onupdate=datetime.now(timezone(timedelta(hours=8))).replace(tzinfo=None))

    user = relationship("User", foreign_keys=[user_id], back_populates="orders")
    receiver = relationship("User", foreign_keys=[receiver_user_id], back_populates="received_orders")
    payments = relationship("Payment", back_populates="order")