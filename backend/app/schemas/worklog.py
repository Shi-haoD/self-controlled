from pydantic import BaseModel
from datetime import date

class WorkLogCreate(BaseModel):
    work_date: date
    project_name: str
    content: str
    work_hours: float

class WorkLogOut(WorkLogCreate):
    id: int
