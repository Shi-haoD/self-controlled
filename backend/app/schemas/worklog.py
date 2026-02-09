from pydantic import BaseModel
from datetime import date, datetime

# 配置Pydantic以支持ORM模式
from pydantic.config import ConfigDict

config = ConfigDict(from_attributes=True)

class WorkLogCreate(BaseModel):
    work_date: date
    project_id: int = None
    project_name: str = None
    work_content: str
    difficulty: str = None
    urgency: str = None
    work_type: str = None
    planned_hours: float = None
    actual_hours: float
    interference: str = None
    remark: str = None

class WorkLogOut(WorkLogCreate):
    id: int
    user_id: int
    status: int
    create_time: datetime
    update_time: datetime
