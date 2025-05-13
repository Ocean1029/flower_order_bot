from enum import Enum

class StaffRole(str, Enum):
    owner = "owner"
    clerk = "clerk"
    admin = "admin" 