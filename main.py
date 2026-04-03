from fastapi import FastAPI
import models
from datetime import date
from database import engine, SessionLocal
from routers import users, records, dashboard
import crud
import schemas

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Finance Data Processing Backend",
    description="A backend for financial data management with RBAC.",
    version="1.0.0"
)

# Seed initial data if database is empty
def seed_data():
    db = SessionLocal()
    try:
        # Check if users already exist
        if not crud.get_users(db):
            # Create default users with realistic Indian names
            admin_user = schemas.UserCreate(
                username="amit_sharma_admin", 
                email="amit.sharma@zorvyn-finance.in", 
                role=models.UserRole.ADMIN, 
                status=models.UserStatus.ACTIVE
            )
            analyst_user = schemas.UserCreate(
                username="priya_nair_analyst", 
                email="priya.nair@zorvyn-finance.in", 
                role=models.UserRole.ANALYST, 
                status=models.UserStatus.ACTIVE
            )
            viewer_user = schemas.UserCreate(
                username="rahul_v_auditor", 
                email="rahul.verma@zorvyn-finance.in", 
                role=models.UserRole.VIEWER, 
                status=models.UserStatus.ACTIVE
            )
            
            u1 = crud.create_user(db, admin_user)
            u2 = crud.create_user(db, analyst_user)
            u3 = crud.create_user(db, viewer_user)
            
            # Create a set of realistic Indian financial records
            records = [
                schemas.RecordCreate(amount=75500.00, type=models.RecordType.INCOME, category="Professional Services", date=date.today(), description="IT Consulting Fee - Project Bengaluru"),
                schemas.RecordCreate(amount=12450.50, type=models.RecordType.INCOME, category="Investment", date=date.today(), description="Fixed Deposit Interest Payout"),
                schemas.RecordCreate(amount=4500.00, type=models.RecordType.EXPENSE, category="Utilities", date=date.today(), description="BESCOM Electricity Bill - March"),
                schemas.RecordCreate(amount=1250.75, type=models.RecordType.EXPENSE, category="Food", date=date.today(), description="Team Dinner at Barbeque Nation"),
                schemas.RecordCreate(amount=350.00, type=models.RecordType.EXPENSE, category="Travel", date=date.today(), description="Uber - Client Meeting Visit"),
                schemas.RecordCreate(amount=45000.00, type=models.RecordType.EXPENSE, category="Rent", date=date.today(), description="Monthly Office Rent - HSR Layout"),
                schemas.RecordCreate(amount=2500.00, type=models.RecordType.EXPENSE, category="Compliance", date=date.today(), description="Professional Tax & TDS Filing")
            ]
            
            for record_data in records:
                crud.create_record(db, record_data, user_id=u1.id)
            
            print("Database successfully populated with realistic Indian operational data.")
    finally:
        db.close()

seed_data()

# Include Routers
app.include_router(users.router)
app.include_router(records.router)
app.include_router(dashboard.router)

@app.get("/")
def root():
    return {"message": "Welcome to the Finance Dashboard API. Visit /docs for documentation."}
