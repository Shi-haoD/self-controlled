# app/crud.py
from sqlalchemy.orm import Session
from app import models, schemas

def create_worklog(db: Session, data: schemas.WorkLogCreate):
    obj = models.WorkLog(**data.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def list_worklogs(db: Session):
    return db.query(models.WorkLog).all()
