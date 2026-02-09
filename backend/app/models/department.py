from sqlalchemy import Column, Integer, String, DateTime, Text, SmallInteger, ForeignKey
from app.models.base import Base
from datetime import datetime


class Department(Base):
    __tablename__ = "sys_department"

    id = Column(Integer, primary_key=True, index=True, comment="部门ID")
    dept_name = Column(String(100), nullable=False, comment="部门名称")
    dept_code = Column(String(50), unique=True, nullable=False, comment="部门编码")
    parent_id = Column(Integer, ForeignKey("sys_department.id"), comment="上级部门ID")
    dept_level = Column(Integer, default=1, comment="部门层级")
    dept_desc = Column(Text, comment="部门描述")
    manager_id = Column(Integer, ForeignKey("sys_user.id"), comment="部门负责人ID")
    sort_order = Column(Integer, default=0, comment="排序序号")
    status = Column(SmallInteger, default=1, comment="部门状态：1-启用，0-禁用")
    create_time = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    update_time = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")