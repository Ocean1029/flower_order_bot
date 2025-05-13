from pydantic import BaseModel

class StatsOut(BaseModel):
    today_orders: int
    pending_orders: int
    monthly_income: float
    total_customers: int
