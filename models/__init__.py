from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import os

Base = declarative_base() 

# 判斷是否有 DATABASE_URL（Render 在部署時會自動注入）
db_url = os.getenv("DATABASE_URL", "sqlite:///messages.db")

# 修正 Render 的 PostgreSQL URL 格式
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

engine = create_engine(db_url, echo=False)

# 如果第一次執行，則會自動建立資料表，而如果資料表已存在，則不會重建
Base.metadata.create_all(engine)

SessionLocal = sessionmaker(bind=engine)
