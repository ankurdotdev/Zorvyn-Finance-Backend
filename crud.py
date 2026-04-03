from sqlalchemy.orm import Session
from sqlalchemy import func
import models
import schemas
from datetime import date

# --- User CRUD ---

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user_update: schemas.UserUpdate):
    db_user = get_user(db, user_id)
    if db_user:
        for key, value in user_update.dict(exclude_unset=True).items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user

# --- Record CRUD ---

def get_record(db: Session, record_id: int):
    return db.query(models.FinancialRecord).filter(models.FinancialRecord.id == record_id).first()

def get_records(db: Session, skip: int = 0, limit: int = 100, 
                type: str = None, category: str = None, 
                start_date: date = None, end_date: date = None):
    query = db.query(models.FinancialRecord)
    if type:
        query = query.filter(models.FinancialRecord.type == type)
    if category:
        query = query.filter(models.FinancialRecord.category == category)
    if start_date:
        query = query.filter(models.FinancialRecord.date >= start_date)
    if end_date:
        query = query.filter(models.FinancialRecord.date <= end_date)
    return query.offset(skip).limit(limit).all()

def create_record(db: Session, record: schemas.RecordCreate, user_id: int):
    db_record = models.FinancialRecord(**record.dict(), user_id=user_id)
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

def update_record(db: Session, record_id: int, record_update: schemas.RecordUpdate):
    db_record = get_record(db, record_id)
    if db_record:
        for key, value in record_update.dict(exclude_unset=True).items():
            setattr(db_record, key, value)
        db.commit()
        db.refresh(db_record)
    return db_record

def delete_record(db: Session, record_id: int):
    db_record = get_record(db, record_id)
    if db_record:
        db.delete(db_record)
        db.commit()
    return db_record

# --- Dashboard Analytics ---

def get_dashboard_summary(db: Session):
    # Total Income
    total_income = db.query(func.sum(models.FinancialRecord.amount))\
                    .filter(models.FinancialRecord.type == models.RecordType.INCOME).scalar() or 0.0
    # Total Expenses
    total_expenses = db.query(func.sum(models.FinancialRecord.amount))\
                    .filter(models.FinancialRecord.type == models.RecordType.EXPENSE).scalar() or 0.0
    # Total Transactions
    total_transactions = db.query(func.count(models.FinancialRecord.id)).scalar() or 0
    
    return {
        "total_income": total_income,
        "total_expenses": total_expenses,
        "net_balance": total_income - total_expenses,
        "total_transactions": total_transactions
    }

def get_category_breakdown(db: Session):
    results = db.query(models.FinancialRecord.category, func.sum(models.FinancialRecord.amount))\
                .group_by(models.FinancialRecord.category).all()
    return [{"category": r[0], "total": r[1]} for r in results]

def get_recent_activity(db: Session, limit: int = 5):
    return db.query(models.FinancialRecord).order_by(models.FinancialRecord.date.desc()).limit(limit).all()
