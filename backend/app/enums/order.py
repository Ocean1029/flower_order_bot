from enum import Enum

class OrderDraftStatus(str, Enum):
    collecting = "collecting"
    abandoned = "abandoned"
    completed = "completed"

class OrderStatus(str, Enum):
    pending = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"
    completed = "completed" 