# app/main.py
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app import models, schemas, crud

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Report Platform")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"msg": "backend running"}

@app.post("/worklogs", summary="测试接口", response_model=schemas.WorkLogOut)
def create_worklog(data: schemas.WorkLogCreate, db: Session = Depends(get_db)):
    return crud.create_worklog(db, data)

@app.get("/worklogs", summary="测试接口2", response_model=list[schemas.WorkLogOut])
def list_worklogs(db: Session = Depends(get_db)):
    return crud.list_worklogs(db)
