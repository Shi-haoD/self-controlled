from sqlalchemy import Column, Integer, String, Date, Numeric, ForeignKey, DateTime, Text, SmallInteger
from app.models.base import Base
from datetime import datetime


class WorkDaily(Base):
    __tablename__ = "work_daily"

    id = Column(Integer, primary_key=True, comment="工作记录ID")
    user_id = Column(Integer, ForeignKey("sys_user.id"), nullable=False, comment="用户ID")
    work_date = Column(Date, nullable=False, comment="工作日期")
    project_id = Column(Integer, ForeignKey("project_info.id"), comment="项目ID")
    project_name = Column(String(200), comment="项目名称")
    work_content = Column(Text, nullable=False, comment="工作内容")
    difficulty = Column(String(20), comment="难度等级")
    urgency = Column(String(20), comment="紧急程度")
    work_type = Column(String(50), comment="工作类型")
    planned_hours = Column(Numeric(5, 1), comment="计划工时")
    actual_hours = Column(Numeric(5, 1), nullable=False, comment="实际工时")
    interference = Column(Text, comment="干扰因素")
    remark = Column(Text, comment="备注说明")
    status = Column(SmallInteger, default=1, comment="状态：1-正常，0-删除")
    create_time = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    update_time = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")
