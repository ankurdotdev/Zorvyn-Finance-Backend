from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from database import get_db
import crud
import schemas
import auth
from models import RecordType

router = APIRouter(
    prefix="/records",
    tags=["Records"]
)

@router.post("/", response_model=schemas.Record, dependencies=[Depends(auth.require_admin)])
def create_record(record: schemas.RecordCreate, db: Session = Depends(get_db), current_user = Depends(auth.require_admin)):
    return crud.create_record(db=db, record=record, user_id=current_user.id)

@router.get("/", response_model=List[schemas.Record], dependencies=[Depends(auth.require_analyst_or_admin)])
def read_records(
    skip: int = 0, 
    limit: int = 100, 
    type: Optional[RecordType] = None, 
    category: Optional[str] = None, 
    start_date: Optional[date] = None, 
    end_date: Optional[date] = None, 
    db: Session = Depends(get_db)
):
    return crud.get_records(db, skip=skip, limit=limit, type=type, category=category, start_date=start_date, end_date=end_date)

@router.get("/{record_id}", response_model=schemas.Record, dependencies=[Depends(auth.require_analyst_or_admin)])
def read_record(record_id: int, db: Session = Depends(get_db)):
    db_record = crud.get_record(db, record_id=record_id)
    if db_record is None:
        raise HTTPException(status_code=404, detail="Record not found")
    return db_record

@router.put("/{record_id}", response_model=schemas.Record, dependencies=[Depends(auth.require_admin)])
def update_record(record_id: int, record_update: schemas.RecordUpdate, db: Session = Depends(get_db)):
    db_record = crud.update_record(db, record_id=record_id, record_update=record_update)
    if db_record is None:
        raise HTTPException(status_code=404, detail="Record not found")
    return db_record

@router.delete("/{record_id}", response_model=schemas.Record, dependencies=[Depends(auth.require_admin)])
def delete_record(record_id: int, db: Session = Depends(get_db)):
    db_record = crud.delete_record(db, record_id=record_id)
    if db_record is None:
        raise HTTPException(status_code=404, detail="Record not found")
    return db_record
