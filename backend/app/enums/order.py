from enum import Enum

class OrderDraftStatus(str, Enum):
    COLLECTING = "collecting"
    ABANDONED = "abandoned"
    COMPLETED = "completed"

class OrderStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed" 