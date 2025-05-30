from app.core.database import Base
from sqlalchemy import (
    Column, Integer, String, Boolean, Text, DateTime, SmallInteger,
    ForeignKey, Numeric
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime, timezone, timedelta
from app.enums.payment import PaymentStatus
from sqlalchemy import Enum as SAEnum


class Payment(Base):
    __tablename__ = "payment"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("order.id"))
    status: Mapped[str] = mapped_column(
        SAEnum(PaymentStatus, name="payment_status", validate_strings=True),
        default=PaymentStatus.PENDING
    )
    method_id: Mapped[int] = mapped_column(ForeignKey("payment_method.id"))
    amount: Mapped[float] = mapped_column(Numeric(10, 2))
    screenshot_url: Mapped[str] = mapped_column(Text, nullable=True)
    paid_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    confirmed_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone(timedelta(hours=8))).replace(tzinfo=None))
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone(timedelta(hours=8))).replace(tzinfo=None), onupdate=datetime.now(timezone(timedelta(hours=8))).replace(tzinfo=None))
    
    order = relationship("Order", back_populates="payments")
    method = relationship("PaymentMethod", backref="payments")

class PaymentMethod(Base):
    __tablename__ = "payment_method"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String, unique=True)
    display_name: Mapped[str] = mapped_column(String)
    display_image_url: Mapped[str] = mapped_column(Text, nullable=True)
    instructions: Mapped[str] = mapped_column(Text, nullable=True)
    requires_manual_confirm: Mapped[bool] = mapped_column(Boolean, default=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
