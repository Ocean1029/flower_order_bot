from typing import Optional, Any
from datetime import datetime
from pydantic import BaseModel

from app.enums.order import OrderDraftStatus, OrderStatus
from app.enums.shipment import ShipmentMethod
from typing import Optional
from datetime import datetime

"""
OrderDraft:
- OrderDraftBase
- OrderDraftUpdate
- OrderDraftCreate
- OrderDraftOut

Order:
- OrderBase
- OrderUpdate
- OrderOut
- OrderCreate
"""

class OrderDraftBase(BaseModel):
    # TODO: 待補目前付的錢

    # 收件 / 寄件人
    customer_name: Optional[str] = None
    customer_phone: Optional[str] = None
    receiver_name: Optional[str] = None
    receiver_phone: Optional[str] = None

    # 付款資訊
    total_amount: Optional[float] = None

    # 商品資訊
    item: Optional[str] = None
    quantity: Optional[int] = None
    note: Optional[str] = None
    card_message: Optional[str] = None

    # 運送資訊
    shipment_method: Optional[ShipmentMethod] = None
    send_datetime: Optional[datetime] = None
    receipt_address: Optional[str] = None
    delivery_address: Optional[str] = None

    class Config:
        from_attributes = True

class OrderDraftUpdate(OrderDraftBase):
    pay_way_id: Optional[int] = None
    pass

class OrderDraftCreate(OrderDraftBase):
    pay_way_id: Optional[int] = None
    pass

class OrderDraftOut(OrderDraftBase):
    id: int
    order_date: datetime
    order_status: OrderDraftStatus
    pay_way: Optional[str]
    weekday: Optional[str]

class OrderDraftStatusOut(BaseModel):
    id: int
    status: OrderDraftStatus
    order_date: datetime
    weekday: Optional[str] = None

"""
Order:
"""

class OrderBase(BaseModel):
    # 收件 / 寄件人
    customer_name: str
    customer_phone: str
    receiver_name: str
    receiver_phone: str

    # order 狀態
    order_date: datetime
    order_status: OrderStatus

    # 付款資訊
    pay_way_id: Optional[int] = None
    total_amount: float

    # 商品資訊
    item: str
    quantity: int
    note: Optional[str]
    card_message: Optional[str]

    # 運送資訊
    shipment_method: ShipmentMethod
    weekday: str
    send_datetime: datetime
    receipt_address: str
    delivery_address: str
    class Config:
        from_attributes = True

class OrderCreate(OrderBase): # TODO 待修改
    customer_name: str
    customer_phone: str
    receiver_name: Optional[str] = None
    receiver_phone: Optional[str] = None

    # order 狀態
    order_status: OrderStatus = OrderStatus.CONFIRMED

    # 付款資訊
    pay_way_id: Optional[int] = None 
    total_amount: float

    # 商品資訊
    item: str
    quantity: int
    note: Optional[str]
    card_message: Optional[str]

    # 運送資訊
    shipment_method: ShipmentMethod
    send_datetime: datetime
    receipt_address: Optional[str] = None
    delivery_address: Optional[str] = None
    class Config:
        from_attributes = True

class OrderUpdate(BaseModel):
    pass


class OrderOut(OrderBase):
    id: int
    order_date: datetime
    weekday: str
    class Config:
        from_attributes = True



