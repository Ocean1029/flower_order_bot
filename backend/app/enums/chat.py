from enum import Enum

class ChatRoomStage(str, Enum):
    welcome = "welcome"
    idle = "idle"
    waiting_owner = "waiting_owner"
    bot_active = "bot_active"

class ChatMessageStatus(str, Enum):
    sent = "sent"
    pending = "pending"
    failed = "failed"

class ChatMessageDirection(str, Enum):
    incoming = "incoming"
    outgoing_by_bot = "outgoing_by_bot"
    outgoing_by_staff = "outgoing_by_staff" 