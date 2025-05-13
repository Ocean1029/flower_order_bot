from enum import Enum

class StaffRole(str, Enum):
    OWNER = "owner"
    CLERK = "clerk"
    ADMIN = "admin" 