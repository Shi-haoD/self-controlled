from sqlalchemy import Column, Integer, String, Date, DateTime, Text, ForeignKey, SmallInteger
from app.models.base import Base
from datetime import datetime


class AnnualPlan(Base):
    __tablename__ = "annual_plan"

    id = Column(Integer, primary_key=True, comment="计划ID")
    user_id = Column(Integer, ForeignKey("sys_user.id"), nullable=False, comment="用户ID")
    year = Column(Integer, nullable=False, comment="年份")
    month = Column(Integer, nullable=False, comment="月份（1-12）")
    plan_content = Column(Text, nullable=False, comment="计划内容")
    target = Column(Text, comment="目标要求")
    result = Column(Text, comment="实际结果")
    completion_status = Column(String(20), default="pending", comment="完成状态")
    difficulty = Column(String(20), comment="难度等级")
    document_url = Column(Text, comment="相关文档链接")
    risk_remark = Column(Text, comment="风险备注")
    start_date = Column(Date, comment="计划开始日期")
    end_date = Column(Date, comment="计划结束日期")
    actual_completion_date = Column(Date, comment="实际完成日期")
    create_time = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    update_time = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")


class WorkProblem(Base):
    __tablename__ = "work_problem"

    id = Column(Integer, primary_key=True, comment="问题ID")
    user_id = Column(Integer, ForeignKey("sys_user.id"), nullable=False, comment="用户ID")
    year = Column(Integer, nullable=False, comment="年份")
    category = Column(String(50), nullable=False, comment="问题分类")
    core_problem = Column(Text, nullable=False, comment="核心问题描述")
    root_cause = Column(Text, comment="根本原因分析")
    rectify_measure = Column(Text, comment="整改措施")
    effect_assessment = Column(Text, comment="效果评估")
    quantified_target = Column(Text, comment="量化目标")
    actual_effect = Column(Text, comment="实际效果")
    improvement_status = Column(String(20), default="open", comment="改进状态")
    follow_up_person = Column(String(50), comment="跟进人")
    resolution_date = Column(Date, comment="解决日期")
    remark = Column(Text, comment="备注说明")
    create_time = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    update_time = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")