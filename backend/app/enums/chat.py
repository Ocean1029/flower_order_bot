from enum import Enum

class ChatRoomStage(str, Enum):
    WELCOME = "WELCOME"
    IDLE = "IDLE"
    ORDER_CONFIRM = "ORDER_CONFIRM"
    WAITING_OWNER = "WAITING_OWNER"
    BOT_ACTIVE = "BOT_ACTIVE"

class ChatMessageStatus(str, Enum):
    SENT = "SENT"
    PENDING = "PENDING"
    FAILED = "FAILED"

class ChatMessageDirection(str, Enum):
    INCOMING = "INCOMING"
    OUTGOING_BY_BOT = "OUTGOING_BY_BOT"
    OUTGOING_BY_STAFF = "OUTGOING_BY_STAFF" 