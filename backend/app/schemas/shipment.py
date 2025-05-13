from typing import Optional
from datetime import datetime
from pydantic import BaseModel

from app.enums.shipment import ShipmentMethod, ShipmentStatus

class ShipmentBase(BaseModel):
    order_id: int
    method: ShipmentMethod
    status: ShipmentStatus = ShipmentStatus.pending
    receiver_user_id: int
    address: Optional[str] = None
    delivery_datetime: Optional[datetime] = None

class ShipmentCreate(ShipmentBase):
    pass

class ShipmentRead(ShipmentBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 