from app.core.database import Base
from sqlalchemy import (
    Column, Integer, String, Boolean, Text, DateTime, SmallInteger,
    ForeignKey, Numeric
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from app.enums import ChatRoomStage, ChatMessageStatus, ChatMessageDirection
from sqlalchemy import Enum as SAEnum


class ChatRoom(Base):
    __tablename__ = "chat_room"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=True)
    assigned_staff_id: Mapped[int] = mapped_column(ForeignKey("staff_user.id"), nullable=True)
    stage: Mapped[ChatRoomStage] = mapped_column(
        SAEnum(ChatRoomStage, name="chat_room_stage", validate_strings=True),
        default=ChatRoomStage.WELCOME
    )
    bot_step: Mapped[int] = mapped_column(SmallInteger, default=0)
    last_message_ts: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    unread_count: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    messages = relationship("ChatMessage", back_populates="room")
    user = relationship("User", back_populates="chat_rooms")
    assigned_staff = relationship("StaffUser", backref="assigned_rooms")
    order_drafts = relationship("OrderDraft", back_populates="room")
    

class ChatMessage(Base):
    __tablename__ = "chat_message"

    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("chat_room.id"))
    status : Mapped[ChatMessageStatus] = mapped_column(
        SAEnum(ChatMessageStatus, name="chat_message_status", validate_strings=True),
        default=ChatMessageStatus.SENT
    )
    direction: Mapped[ChatMessageDirection] = mapped_column(
        SAEnum(ChatMessageDirection, name="chat_message_direction", validate_strings=True),
    )
    text: Mapped[str] = mapped_column(Text)
    image_url: Mapped[str] = mapped_column(Text, nullable=True)
    line_msg_id: Mapped[str] = mapped_column(String, nullable=True)
    processed: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    room = relationship("ChatRoom", back_populates="messages")
