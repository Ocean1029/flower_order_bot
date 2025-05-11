# models/__init__.py
from core.database import Base  # 供 Alembic 使用

# 依需求 import 各資料表檔案，使其在匯入時註冊到 Base
# from .user import User
# from .staff import StaffUser
# from .chat import ChatRoom, ChatMessage
# from .order import Order, OrderDraft
# from .payment import Payment, PaymentMethod
# from .logistics import Shipment
# from .notification import Notification
# from .audit import AuditLog

# __all__ = (
#     "User",
#     "StaffUser",
#     "ChatRoom",
#     "ChatMessage",
#     "Order",
#     "OrderDraft",
#     "Payment",
#     "PaymentMethod",
#     "Shipment",
#     "Notification",
#     "AuditLog",
# )

from .user import User
from .order import Order
from .message import Message

__all__ = (
    "User",
    "Order",
    "Message"
)
