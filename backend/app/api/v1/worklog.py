from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.worklog import WorkLogCreate
from app.models.worklog import WorkLog

router = APIRouter(prefix="/worklog", tags=["WorkLog"])

@router.get("")
def list_worklogs(db: Session = Depends(get_db)):
    return db.query(WorkLog).all()

@router.post("")
def create_worklog(data: WorkLogCreate, db: Session = Depends(get_db)):
    obj = WorkLog(**data.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj
