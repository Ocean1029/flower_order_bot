from core.database import Base
from sqlalchemy import (
    Column, Integer, String, Boolean, Text, DateTime, SmallInteger,
    ForeignKey, Numeric
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime

class ChatRoom(Base):
    __tablename__ = "chat_room"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=True)
    assigned_staff_id: Mapped[int] = mapped_column(ForeignKey("staff_user.id"), nullable=True)
    stage: Mapped[str] = mapped_column(String, default="welcome")
    bot_step: Mapped[int] = mapped_column(SmallInteger, default=0)
    last_message_ts: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    unread_count: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ChatMessage(Base):
    __tablename__ = "chat_message"

    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("chat_room.id"))
    status: Mapped[str] = mapped_column(String, default="sent")
    direction: Mapped[str] = mapped_column(String)
    text: Mapped[str] = mapped_column(Text)
    image_url: Mapped[str] = mapped_column(Text, nullable=True)
    line_msg_id: Mapped[str] = mapped_column(String, nullable=True)
    processed: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
