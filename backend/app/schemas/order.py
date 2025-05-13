from typing import Optional, Any
from datetime import datetime
from pydantic import BaseModel

from app.enums.order import OrderDraftStatus, OrderStatus
from app.enums.shipment import ShipmentMethod

class OrderDraftBase(BaseModel):
    room_id: int
    user_id: int
    status: OrderDraftStatus = OrderDraftStatus.collecting
    payload_json: Any

class OrderDraftCreate(OrderDraftBase):
    pass

class OrderDraftRead(OrderDraftBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class OrderBase(BaseModel):
    user_id: int
    draft_id: int
    status: OrderStatus = OrderStatus.pending
    item_type: str
    product_name: str
    quantity: int
    notes: Optional[str] = None
    card_message: Optional[str] = None
    receipt_address: Optional[str] = None
    total_amount: float

class OrderCreate(OrderBase):
    shipment_method: ShipmentMethod = ShipmentMethod.store_pickup  # 便於一次下單時帶入

class OrderRead(OrderBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 