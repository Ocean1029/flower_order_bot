from typing import Optional, Any
from datetime import datetime
from pydantic import BaseModel

from app.enums.order import OrderDraftStatus, OrderStatus
from app.enums.shipment import ShipmentMethod

class OrderDraftBase(BaseModel):
    room_id: int
    user_id: int
    status: OrderDraftStatus = OrderDraftStatus.COLLECTING

class OrderDraftCreate(OrderDraftBase):
    pass

class OrderDraftRead(OrderDraftBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True



class OrderCreate(BaseModel):
    customer_name: str
    phone: str
    flower: str
    qty: int
    budget: float
    pickup_method: str
    pickup_date: str  # 若為 datetime 請改為 datetime
    pickup_time: str
    note: Optional[str]

    class Config:
        orm_mode = True

class OrderOut(BaseModel):
    id: int
    customer_name: str
    customer_phone: str
    receipt_address: str
    order_date: datetime
    total_amount: float
    item: str
    quantity: int
    note: Optional[str]
    pay_way: str
    card_message: Optional[str]
    weekday: str
    send_datetime: datetime
    receiver_name: str
    receiver_phone: str
    delivery_address: str
    order_status: OrderStatus
    shipment_method: ShipmentMethod
    
    class Config:
        orm_mode = True


"""
order_form_fields = {
    "order_info": {
        "customer_name": "YOUR NAME",
        "customer_phone": "YOURMOBILE",
        "receipt_address": "收據寄送地址",
        "order_date": "Timestamp",
        "total_amount": "TOTAL",
        "item": "ITEM",
        "quantity": "QTY",
        "note": "備註",
        "pay_way": "PAY WAY",
        "card_message": "卡片內容"
    },
    "delivery_info": {
        "weekday": "星期",
        "send_datetime": "送禮日期&時間",
        "receiver_name": "RECEIVER NAME",
        "receiver_phone": "MOBILE",
        "delivery_address": "ADD"
    }
}
"""