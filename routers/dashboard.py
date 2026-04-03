from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import crud
import schemas
import auth

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
    dependencies=[Depends(auth.require_any_role)] # Admin, Analyst, and Viewer can access
)

@router.get("/analytics", response_model=schemas.DashboardAnalytics)
def get_dashboard_analytics(db: Session = Depends(get_db)):
    summary = crud.get_dashboard_summary(db)
    category_breakdown = crud.get_category_breakdown(db)
    recent_activity = crud.get_recent_activity(db)
    
    return {
        "summary": summary,
        "category_breakdown": category_breakdown,
        "recent_activity": recent_activity
    }
