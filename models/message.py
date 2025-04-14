from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from datetime import datetime
from . import Base

class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    text = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    used = Column(Boolean, default=False)
