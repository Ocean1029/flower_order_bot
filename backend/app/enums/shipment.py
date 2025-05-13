from enum import Enum

class ShipmentMethod(str, Enum):
    STORE_PICKUP = "store_pickup"
    DELIVERY = "delivery"

class ShipmentStatus(str, Enum):
    PENDING = "pending"
    DISPATCHED = "dispatched"
    DELIVERED = "delivered"
    RETURNED = "returned" 