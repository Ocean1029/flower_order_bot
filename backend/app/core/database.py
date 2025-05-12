# core/database.py
import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv

load_dotenv()

# ─────────────── 讀取連線字串 ───────────────
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///messages.db")
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+asyncpg://", 1)

# ─────────────── 建立 Engine / Session ───────────────
engine = create_async_engine(DATABASE_URL, future=True, echo=False)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)
Base = declarative_base()

async def get_db() -> AsyncSession :
    async with AsyncSessionLocal() as session:
        yield session