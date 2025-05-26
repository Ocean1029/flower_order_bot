from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.enums.chat import ChatRoomStage, ChatMessageStatus, ChatMessageDirection

class LastMessage(BaseModel):
    text: str
    timestamp: datetime

class ChatRoomOut(BaseModel):
    room_id: int
    user_name: str
    user_avatar_url: Optional[str] = None
    unread_count: int
    status: ChatRoomStage
    last_message: Optional[LastMessage]

class ChatMessageBase(BaseModel):
    text: Optional[str] = None
    image_url: Optional[str] = None


class ChatMessageOut(BaseModel):
    id: int
    user_avatar_url: Optional[str] = None
    direction: ChatMessageDirection
    message: ChatMessageBase
    status: ChatMessageStatus
    created_at: datetime
