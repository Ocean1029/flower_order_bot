from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from app.models.order import Order
from app.models.user import User

async def get_stats(session: AsyncSession):
    now = datetime.utcnow()
    today_start = datetime(now.year, now.month, now.day)
    month_start = datetime(now.year, now.month, 1)

    # 今日訂單數量
    today_stmt = select(func.count()).where(Order.created_at >= today_start)
    today_orders = (await session.execute(today_stmt)).scalar()

    # 總顧客數
    customer_stmt = select(func.count()).select_from(User)
    total_customers = (await session.execute(customer_stmt)).scalar()

    # 當月營收
    income_stmt = select(func.coalesce(func.sum(Order.total_amount), 0)).where(Order.created_at >= month_start)
    monthly_income = (await session.execute(income_stmt)).scalar()

    pending_stmt = select(func.count()).select_from(Order)
    pending_orders = (await session.execute(pending_stmt)).scalar()

    return {
        "today_orders": today_orders,
        "pending_orders": pending_orders,
        "monthly_income": float(monthly_income or 0),
        "total_customers": total_customers
    }
