from sqlalchemy import Column, Integer, String, Date, Numeric, ForeignKey
from app.models.base import Base

class WorkLog(Base):
    __tablename__ = "work_daily"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("sys_user.id"))
    work_date = Column(Date)
    project_name = Column(String(200))
    content = Column(String)
    work_hours = Column(Numeric(5, 1))
