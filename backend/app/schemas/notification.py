from typing import Optional, Any
from datetime import datetime
from pydantic import BaseModel

from app.enums.notification import NotificationReceiverType, NotificationStatus

class NotificationBase(BaseModel):
    receiver_type: NotificationReceiverType
    receiver_id: int
    channel: str
    payload: Any
    status: NotificationStatus = NotificationStatus.queued
    send_at: Optional[datetime] = None

class NotificationCreate(NotificationBase):
    pass

class NotificationRead(NotificationBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True 