from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field

from app.enums.user import StaffRole

class UserBase(BaseModel):
    line_uid: Optional[str] = None
    name: Optional[str] = None
    phone: Optional[str] = None
    avatar_url: Optional[str] = None

class UserCreate(UserBase):
    pass


class StaffBase(BaseModel):
    line_uid: str
    name: str
    role: StaffRole = Field(default=StaffRole.CLERK)

class StaffCreate(StaffBase):
    password: str = Field(alias="password_hash")

class StaffRead(StaffBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 