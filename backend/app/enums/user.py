from enum import Enum

class StaffRole(str, Enum):
    OWNER = "OWNER"
    CLERK = "CLERK"
    ADMIN = "ADMIN" 