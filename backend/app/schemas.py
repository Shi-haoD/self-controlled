# app/schemas.py
from pydantic import BaseModel
from typing import Optional, Dict
from datetime import date

class WorkLogCreate(BaseModel):
    user_name: str
    work_date: date
    work_hours: float
    content: Optional[str] = None
    extra_data: Optional[Dict] = None

class WorkLogOut(WorkLogCreate):
    id: str