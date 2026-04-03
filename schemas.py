from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import date
from models import UserRole, UserStatus, RecordType

# --- User Schemas ---

class UserBase(BaseModel):
    username: str
    email: EmailStr
    role: UserRole = UserRole.VIEWER
    status: UserStatus = UserStatus.ACTIVE

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[UserRole] = None
    status: Optional[UserStatus] = None

class User(UserBase):
    id: int

    class Config:
        from_attributes = True

# --- Financial Record Schemas ---

class RecordBase(BaseModel):
    amount: float = Field(..., gt=0)
    type: RecordType
    category: str
    date: date
    description: Optional[str] = None

class RecordCreate(RecordBase):
    pass

class RecordUpdate(BaseModel):
    amount: Optional[float] = Field(None, gt=0)
    type: Optional[RecordType] = None
    category: Optional[str] = None
    date: Optional[date] = None
    description: Optional[str] = None

class Record(RecordBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True

# --- Dashboard Schemas ---

class DashboardSummary(BaseModel):
    total_income: float
    total_expenses: float
    net_balance: float
    total_transactions: int

class CategoryTotal(BaseModel):
    category: str
    total: float

class DashboardAnalytics(BaseModel):
    summary: DashboardSummary
    category_breakdown: List[CategoryTotal]
    recent_activity: List[Record]
