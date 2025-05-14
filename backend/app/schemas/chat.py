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
    unread_count: int
    status: ChatRoomStage
    last_message: Optional[LastMessage]

class ChatMessageOut(BaseModel):
    id: int
    direction: ChatMessageDirection
    text: Optional[str]
    image_url: Optional[str]
    status: ChatMessageStatus
    line_msg_id: Optional[str]
    processed: bool
    created_at: datetime

class ChatMessageCreate(BaseModel):
    direction: ChatMessageDirection
    text: Optional[str] = None
    image_url: Optional[str] = None

class ChatRoomModeSwitch(BaseModel):
    mode: ChatRoomStage