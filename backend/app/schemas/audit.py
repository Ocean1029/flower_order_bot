from typing import Optional, Any
from datetime import datetime
from pydantic import BaseModel

class AuditLogRead(BaseModel):
    id: int
    staff_id: int
    action: str
    target_table: str
    target_id: int
    diff: Optional[Any] = None
    logged_at: datetime

    class Config:
        from_attributes = True 