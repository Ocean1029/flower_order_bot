from core.database import Base
from sqlalchemy import (
    Column, Integer, String, Boolean, Text, DateTime, SmallInteger,
    ForeignKey, Numeric
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime

from enum import Enum
from sqlalchemy import Enum as SAEnum

class NotificationReceiverType(str, Enum):
    USER = "user"
    STAFF = "staff"

class NotificationChannel(str, Enum):
    LINE = "line"
    EMAIL = "email"
    SMS = "sms"

class NotificationStatus(str, Enum):
    QUEUED = "queued"
    SENT = "sent"
    FAILED = "failed"

class Notification(Base):
    __tablename__ = "notification"

    id: Mapped[int] = mapped_column(primary_key=True)
    receiver_type: Mapped[str] = mapped_column(
        SAEnum(NotificationReceiverType, name="notification_receiver_type", validate_strings=True),
        default=NotificationReceiverType.USER
    )
    receiver_id: Mapped[int] = mapped_column(Integer)
    channel: Mapped[str] = mapped_column(
        SAEnum(NotificationChannel, name="notification_channel", validate_strings=True),
        default=NotificationChannel.LINE
    )
    status: Mapped[str] = mapped_column(
        SAEnum(NotificationStatus, name="notification_status", validate_strings=True),
        default=NotificationStatus.QUEUED
    )
    payload: Mapped[str] = mapped_column(Text)
    send_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class AuditLog(Base):
    __tablename__ = "audit_log"

    id: Mapped[int] = mapped_column(primary_key=True)
    staff_id: Mapped[int] = mapped_column(ForeignKey("staff_user.id"))
    action: Mapped[str] = mapped_column(String)
    target_table: Mapped[str] = mapped_column(String)
    target_id: Mapped[int] = mapped_column(Integer)
    diff: Mapped[str] = mapped_column(Text, nullable=True)
    logged_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
