from typing import Optional, Any
from datetime import datetime
from pydantic import BaseModel

from app.enums.order import OrderDraftStatus, OrderStatus
from app.enums.shipment import ShipmentMethod

from typing import Optional
from datetime import datetime

class OrderDraftOut(BaseModel):
    id: int

    # 收件 / 寄件人
    customer_name: Optional[str] = None
    customer_phone: Optional[str] = None
    receiver_name: Optional[str] = None
    receiver_phone: Optional[str] = None

    # order 狀態
    order_date: Optional[datetime] = None
    order_status: Optional[OrderDraftStatus] = None

    # 付款資訊
    pay_way: Optional[str] = None
    total_amount: Optional[float] = None

    # 商品資訊
    item: Optional[str] = None
    quantity: Optional[int] = None
    note: Optional[str] = None
    card_message: Optional[str] = None

    # 運送資訊
    shipment_method: Optional[ShipmentMethod] = None
    weekday: Optional[str] = None
    send_datetime: Optional[datetime] = None
    receipt_address: Optional[str] = None
    delivery_address: Optional[str] = None

    class Config:
        orm_mode = True

class OrderOut(BaseModel):
    id: int
    # 收件 / 寄件人
    customer_name: str
    customer_phone: str
    receiver_name: str
    receiver_phone: str

    # order 狀態
    order_date: datetime
    order_status: OrderStatus

    # 付款資訊
    pay_way: str
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
        orm_mode = True

class OrderDraftUpdate(BaseModel):
    # 收件 / 寄件人
    customer_name: Optional[str] = None
    customer_phone: Optional[str] = None
    receiver_name: Optional[str] = None
    receiver_phone: Optional[str] = None

    # order 狀態
    order_date: Optional[datetime] = None
    order_status: Optional[OrderDraftStatus] = None

    # 付款資訊
    pay_way: Optional[str] = None
    total_amount: Optional[float] = None

    # 商品資訊
    item: Optional[str] = None
    quantity: Optional[int] = None
    note: Optional[str] = None
    card_message: Optional[str] = None

    # 運送資訊
    shipment_method: Optional[ShipmentMethod] = None
    weekday: Optional[str] = None
    send_datetime: Optional[datetime] = None
    receipt_address: Optional[str] = None
    delivery_address: Optional[str] = None