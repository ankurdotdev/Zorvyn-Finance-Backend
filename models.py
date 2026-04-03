from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum
from database import Base

class UserRole(str, enum.Enum):
    ADMIN = "ADMIN"
    ANALYST = "ANALYST"
    VIEWER = "VIEWER"

class UserStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"

class RecordType(str, enum.Enum):
    INCOME = "INCOME"
    EXPENSE = "EXPENSE"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    role = Column(Enum(UserRole), default=UserRole.VIEWER)
    status = Column(Enum(UserStatus), default=UserStatus.ACTIVE)

    records = relationship("FinancialRecord", back_populates="owner")

class FinancialRecord(Base):
    __tablename__ = "financial_records"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    type = Column(Enum(RecordType), nullable=False)
    category = Column(String, index=True)
    date = Column(Date, nullable=False)
    description = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="records")
