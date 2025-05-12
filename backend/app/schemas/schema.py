from __future__ import annotations

"""Pydantic schemas used by FastAPI.
每個 *Base 只含可共用欄位，*Create 代表新增資料時需要的欄位，
*Read 代表回傳給前端的完整資料（含 id / timestamp）。
若有巢狀關係（如 Order ⟶ Shipment / Payment）可在 *Read 使用巢狀模型。
"""

from enum import Enum
from typing import Optional, List, Any
from datetime import datetime, date

from pydantic import BaseModel, Field, EmailStr

# ──────────────────────────────
# Enum 定義（與 SQLAlchemy Enum 同步）
# ──────────────────────────────

class StaffRole(str, Enum):
    owner = "owner"
    clerk = "clerk"
    admin = "admin"

class ChatRoomStage(str, Enum):
    welcome = "welcome"
    idle = "idle"
    waiting_owner = "waiting_owner"
    bot_active = "bot_active"

class ChatMessageStatus(str, Enum):
    sent = "sent"
    pending = "pending"
    failed = "failed"

class ChatMessageDirection(str, Enum):
    incoming = "incoming"
    outgoing_by_bot = "outgoing_by_bot"
    outgoing_by_staff = "outgoing_by_staff"

class OrderDraftStatus(str, Enum):
    collecting = "collecting"
    abandoned = "abandoned"
    completed = "completed"

class OrderStatus(str, Enum):
    pending = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"
    completed = "completed"

class PaymentStatus(str, Enum):
    pending = "pending"
    paid = "paid"
    failed = "failed"
    refunded = "refunded"

class ShipmentMethod(str, Enum):
    store_pickup = "store_pickup"
    delivery = "delivery"

class ShipmentStatus(str, Enum):
    pending = "pending"
    dispatched = "dispatched"
    delivered = "delivered"
    returned = "returned"

class NotificationReceiverType(str, Enum):
    user = "user"
    staff = "staff"

class NotificationStatus(str, Enum):
    queued = "queued"
    sent = "sent"
    failed = "failed"

# ──────────────────────────────
# A. 顧客與員工
# ──────────────────────────────

class UserBase(BaseModel):
    line_uid: Optional[str] = None
    name: str
    phone: Optional[str] = None

class UserCreate(UserBase):
    pass

class UserRead(UserBase):
    id: int
    has_ordered: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class StaffBase(BaseModel):
    line_uid: str
    name: str
    role: StaffRole = Field(default=StaffRole.clerk)

class StaffCreate(StaffBase):
    password: str = Field(alias="password_hash")

class StaffRead(StaffBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# ──────────────────────────────
# B. 聊天室與訊息
# ──────────────────────────────

class ChatRoomBase(BaseModel):
    user_id: Optional[int] = None
    assigned_staff_id: Optional[int] = None
    stage: ChatRoomStage = ChatRoomStage.welcome
    bot_step: int = 0

class ChatRoomRead(ChatRoomBase):
    id: int
    last_message_ts: Optional[datetime] = None
    unread_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class ChatMessageBase(BaseModel):
    room_id: int
    text: str
    status: ChatMessageStatus = ChatMessageStatus.sent
    direction: ChatMessageDirection
    image_url: Optional[str] = None
    line_msg_id: Optional[str] = None

class ChatMessageCreate(ChatMessageBase):
    pass

class ChatMessageRead(ChatMessageBase):
    id: int
    processed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# ──────────────────────────────
# C. 訂單核心
# ──────────────────────────────

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
        orm_mode = True

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
        orm_mode = True

# Payment
class PaymentBase(BaseModel):
    order_id: int
    status: PaymentStatus = PaymentStatus.pending
    method_id: int
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
        orm_mode = True

# Shipment
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
        orm_mode = True

# PaymentMethod
class PaymentMethodBase(BaseModel):
    code: str
    display_name: str
    display_image_url: Optional[str] = None
    instructions: str
    requires_manual_confirm: bool = True
    active: bool = True
    sort_order: int = 0

class PaymentMethodCreate(PaymentMethodBase):
    pass

class PaymentMethodRead(PaymentMethodBase):
    id: int

    class Config:
        orm_mode = True

# ──────────────────────────────
# D. 自動化與營運
# ──────────────────────────────

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
        orm_mode = True

class AuditLogRead(BaseModel):
    id: int
    staff_id: int
    action: str
    target_table: str
    target_id: int
    diff: Optional[Any] = None
    logged_at: datetime

    class Config:
        orm_mode = True
