from sqlalchemy import Column, Integer, String
from . import Base
from datetime import datetime
from sqlalchemy import DateTime, ForeignKey

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    line_id = Column(String, unique=True)
    customer_name = Column(String)
    phone_number = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

