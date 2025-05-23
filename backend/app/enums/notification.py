from enum import Enum

class NotificationReceiverType(str, Enum):
    USER = "USER"
    STAFF = "STAFF"

class NotificationStatus(str, Enum):
    QUEUED = "QUEUED"
    SENT = "SENT"
    FAILED = "FAILED" 

class NotificationChannel(str, Enum):
    LINE = "LINE"
    EMAIL = "EMAIL"
    SMS = "SMS"