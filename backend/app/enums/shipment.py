from enum import Enum

class ShipmentMethod(str, Enum):
    STORE_PICKUP = "STORE_PICKUP"
    DELIVERY = "DELIVERY"

class ShipmentStatus(str, Enum):
    PENDING = "PENDING"
    DISPATCHED = "DISPATCHED"
    DELIVERED = "DELIVERED"
    RETURNED = "RETURNED" 