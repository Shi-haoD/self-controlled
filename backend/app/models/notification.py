from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, SmallInteger
from sqlalchemy.dialects.postgresql import JSONB
from app.models.base import Base
from datetime import datetime


class SysMessage(Base):
    __tablename__ = "sys_message"

    id = Column(Integer, primary_key=True, comment="消息ID")
    sender_id = Column(Integer, ForeignKey("sys_user.id"), comment="发送者ID")
    receiver_id = Column(Integer, ForeignKey("sys_user.id"), nullable=False, comment="接收者ID")
    title = Column(String(200), nullable=False, comment="消息标题")
    content = Column(Text, nullable=False, comment="消息内容")
    msg_type = Column(String(50), nullable=False, comment="消息类型")
    priority = Column(String(20), default="normal", comment="优先级")
    is_read = Column(SmallInteger, default=0, comment="是否已读：0-未读，1-已读")
    read_time = Column(DateTime, comment="阅读时间")
    related_id = Column(Integer, comment="关联业务ID")
    related_type = Column(String(50), comment="关联业务类型")
    create_time = Column(DateTime, default=datetime.utcnow, comment="创建时间")


class WorkTask(Base):
    __tablename__ = "work_task"

    id = Column(Integer, primary_key=True, comment="任务ID")
    publisher_id = Column(Integer, ForeignKey("sys_user.id"), nullable=False, comment="发布者ID")
    receiver_id = Column(Integer, ForeignKey("sys_user.id"), nullable=False, comment="接收者ID")
    task_content = Column(Text, nullable=False, comment="任务内容")
    task_type = Column(String(50), default="general", comment="任务类型")
    priority = Column(String(20), default="medium", comment="优先级")
    deadline = Column(DateTime, nullable=False, comment="截止日期")
    estimated_hours = Column(Integer, comment="预估工时")
    actual_hours = Column(Integer, comment="实际工时")
    status = Column(String(20), default="assigned", comment="任务状态")
    completion_description = Column(Text, comment="完成情况描述")
    attachment_urls = Column(JSONB, comment="附件URL数组")
    create_time = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    update_time = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")
    completed_time = Column(DateTime, comment="完成时间")
