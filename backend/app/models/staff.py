from app.core.database import Base
from sqlalchemy import (
    Column, Integer, String, Boolean, Text, DateTime, SmallInteger,
    ForeignKey, Numeric
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime, timezone, timedelta
from app.enums.user import StaffRole
from sqlalchemy import Enum as SAEnum


class StaffUser(Base):
    __tablename__ = "staff_user"

    id: Mapped[int] = mapped_column(primary_key=True)
    line_uid: Mapped[str] = mapped_column(String, unique=True)
    name: Mapped[str] = mapped_column(String)
    role: Mapped[str] = mapped_column(
        SAEnum(StaffRole, name="staff_role", validate_strings=True),
        default=StaffRole.CLERK
    )
    password_hash: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone(timedelta(hours=8))).replace(tzinfo=None))
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone(timedelta(hours=8))).replace(tzinfo=None), onupdate=datetime.now(timezone(timedelta(hours=8))).replace(tzinfo=None))
