from typing import Optional
from datetime import datetime
from pydantic import BaseModel

from app.enums.payment import PaymentStatus

class PaymentMethodBase(BaseModel):
    id: int
    active: bool = True
    code: str
    display_name: str
    display_image_url: Optional[str] = None
    instructions: str
    requires_manual_confirm: bool = True
    
class PaymentBase(BaseModel):
    order_id: int
    status: PaymentStatus = PaymentStatus.PENDING
    amount: float
    screenshot_url: Optional[str] = None

class PaymentCreate(PaymentBase):
    pass

class PaymentRead(PaymentBase):
    id: int
    paid_at: Optional[datetime] = None
    confirmed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True