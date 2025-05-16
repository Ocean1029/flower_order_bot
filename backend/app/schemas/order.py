from typing import Optional, Any
from datetime import datetime
from pydantic import BaseModel

from app.enums.order import OrderDraftStatus, OrderStatus
from app.enums.shipment import ShipmentMethod, ShipmentStatus

class OrderDraftOut(BaseModel):
    id: int
    # 收件 / 寄件人
    customer_name: str
    customer_phone: str
    receiver_name: str
    receiver_phone: str

    # order 狀態
    order_date: datetime
    order_status: OrderDraftStatus

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

