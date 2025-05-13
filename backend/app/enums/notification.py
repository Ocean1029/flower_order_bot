from enum import Enum

class NotificationReceiverType(str, Enum):
    user = "user"
    staff = "staff"

class NotificationStatus(str, Enum):
    queued = "queued"
    sent = "sent"
    failed = "failed" 