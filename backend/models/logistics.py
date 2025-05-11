from core.database import Base
from sqlalchemy import (
    Column, Integer, String, Boolean, Text, DateTime, SmallInteger,
    ForeignKey, Numeric
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime

from enum import Enum
from sqlalchemy import Enum as SAEnum

class ShipmentMethod(str, Enum):
    STORE_PICKUP = "store_pickup"
    DELIVERY = "delivery"

class ShipmentStatus(str, Enum):
    PENDING = "pending"
    DISPATCHED = "dispatched"
    DELIVERED = "delivered"
    RETURNED = "returned"
    
class Shipment(Base):
    __tablename__ = "shipment"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("order.id"), unique=True)
    method: Mapped[str] = mapped_column(
        SAEnum(ShipmentMethod, name="shipment_method", validate_strings=True),
        default=ShipmentMethod.STORE_PICKUP
    )
    status: Mapped[str] = mapped_column(
        SAEnum(ShipmentStatus, name="shipment_status", validate_strings=True),
        default=ShipmentStatus.PENDING
    )
    receiver_user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    address: Mapped[str] = mapped_column(Text, nullable=True)
    delivery_datetime: Mapped[datetime] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    order = relationship("Order", back_populates="shipment")

