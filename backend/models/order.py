from sqlalchemy import Column, Integer, String, ForeignKey
from . import Base
from datetime import datetime
from sqlalchemy import DateTime, Boolean

class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    flower_type = Column(String)
    quantity = Column(Integer)
    budget = Column(Integer)
    pickup_method = Column(String)
    pickup_date = Column(String)
    pickup_time = Column(String)
    extra_requirements = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
