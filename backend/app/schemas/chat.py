from typing import Optional
from datetime import datetime
from pydantic import BaseModel

from app.enums.chat import ChatRoomStage, ChatMessageStatus, ChatMessageDirection

class ChatRoomBase(BaseModel):
    user_id: Optional[int] = None
    assigned_staff_id: Optional[int] = None
    stage: ChatRoomStage = ChatRoomStage.WELCOME
    bot_step: int = 0

class ChatRoomRead(ChatRoomBase):
    id: int
    last_message_ts: Optional[datetime] = None
    unread_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ChatMessageBase(BaseModel):
    room_id: int
    text: str
    status: ChatMessageStatus = ChatMessageStatus.SENT
    direction: ChatMessageDirection
    image_url: Optional[str] = None
    line_msg_id: Optional[str] = None

class ChatMessageCreate(ChatMessageBase):
    pass

class ChatMessageRead(ChatMessageBase):
    id: int
    processed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 