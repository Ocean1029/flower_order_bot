from enum import Enum

class OrderDraftStatus(str, Enum):
    COLLECTING = "COLLECTING"
    ABANDONED = "ABANDONED"
    COMPLETED = "COMPLETED"

class OrderStatus(str, Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"
    COMPLETED = "COMPLETED" 