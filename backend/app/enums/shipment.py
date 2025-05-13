from enum import Enum

class ShipmentMethod(str, Enum):
    store_pickup = "store_pickup"
    delivery = "delivery"

class ShipmentStatus(str, Enum):
    pending = "pending"
    dispatched = "dispatched"
    delivered = "delivered"
    returned = "returned" 