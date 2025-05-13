from enum import Enum

class NotificationReceiverType(str, Enum):
    USER = "user"
    STAFF = "staff"

class NotificationStatus(str, Enum):
    QUEUED = "queued"
    SENT = "sent"
    FAILED = "failed" 