from enum import Enum

class ChatRoomStage(str, Enum):
    WELCOME = "welcome"
    IDLE = "idle"
    WAITING_OWNER = "waiting_owner"
    BOT_ACTIVE = "bot_active"

class ChatMessageStatus(str, Enum):
    SENT = "sent"
    PENDING = "pending"
    FAILED = "failed"

class ChatMessageDirection(str, Enum):
    INCOMING = "incoming"
    OUTGOING_BY_BOT = "outgoing_by_bot"
    OUTGOING_BY_STAFF = "outgoing_by_staff" 