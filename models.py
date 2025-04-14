from sqlalchemy import Column, Integer, String, DateTime, Boolean, create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import make_url

from datetime import datetime 
import os

Base = declarative_base()

class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    text = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    used = Column(Boolean, default=False)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    line_id = Column(String, unique=True)
    customer_name = Column(String)
    phone_number = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

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

# 判斷是否有 DATABASE_URL（Render 在部署時會自動注入）
db_url = os.getenv("DATABASE_URL", "sqlite:///messages.db")

# 修正 Render 的 PostgreSQL URL 格式
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

engine = create_engine(db_url, echo=False)

# 如果第一次執行，則會自動建立資料表，而如果資料表已存在，則不會重建
Base.metadata.create_all(engine)

SessionLocal = sessionmaker(bind=engine)
