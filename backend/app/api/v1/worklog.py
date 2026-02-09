from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.worklog import WorkLogCreate, WorkLogOut
from app.models.worklog import WorkDaily

router = APIRouter(prefix="/worklog", tags=["工时填报"])

@router.get("")
def list_worklogs(db: Session = Depends(get_db)):
    worklogs = db.query(WorkDaily).all()
    return [WorkLogOut.from_orm(worklog) for worklog in worklogs]

@router.post("")
def create_worklog(data: WorkLogCreate, db: Session = Depends(get_db)):
    obj = WorkDaily(**data.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return WorkLogOut.from_orm(obj)
