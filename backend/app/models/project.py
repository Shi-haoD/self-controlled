from sqlalchemy import Column, Integer, String, Date, DateTime, Text, Numeric, ForeignKey, SmallInteger
from sqlalchemy.dialects.postgresql import JSONB
from app.models.base import Base
from datetime import datetime


class ProjectInfo(Base):
    __tablename__ = "project_info"

    id = Column(Integer, primary_key=True, comment="项目ID")
    project_name = Column(String(200), unique=True, nullable=False, comment="项目名称")
    project_code = Column(String(50), unique=True, comment="项目编码")
    description = Column(Text, comment="项目描述")
    local_path = Column(Text, comment="本地路径")
    online_url = Column(Text, comment="线上地址")
    svn_url = Column(Text, comment="SVN地址")
    git_url = Column(Text, comment="Git仓库地址")
    node_version = Column(String(20), comment="Node版本要求")
    python_version = Column(String(20), comment="Python版本要求")
    java_version = Column(String(20), comment="Java版本要求")
    database_type = Column(String(50), comment="数据库类型")
    leader_id = Column(Integer, ForeignKey("sys_user.id"), comment="项目负责人ID")
    team_members = Column(JSONB, comment="团队成员ID数组")
    start_date = Column(Date, comment="开始日期")
    end_date = Column(Date, comment="预计结束日期")
    actual_end_date = Column(Date, comment="实际结束日期")
    project_status = Column(String(20), default="planning", comment="项目状态")
    priority = Column(String(20), default="medium", comment="优先级")
    budget = Column(Numeric(12, 2), comment="项目预算")
    create_time = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    update_time = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")


class ProjectStatistic(Base):
    __tablename__ = "project_statistic"

    id = Column(Integer, primary_key=True, comment="统计ID")
    project_id = Column(Integer, ForeignKey("project_info.id"), nullable=False, comment="项目ID")
    leader_name = Column(String(50), comment="项目负责人姓名")
    total_hours = Column(Numeric(10, 1), default=0, comment="项目累计工时")
    develop_cycle = Column(Integer, default=0, comment="开发周期（天）")
    bug_count = Column(Integer, default=0, comment="BUG修复次数")
    feature_count = Column(Integer, default=0, comment="功能点数量")
    requirement_count = Column(Integer, default=0, comment="需求数量")
    project_status = Column(String(20), comment="项目状态")
    delivery_quality = Column(String(20), comment="交付质量评级")
    satisfaction_score = Column(Numeric(3, 1), comment="满意度评分（1-10分）")
    risk_level = Column(String(20), default="low", comment="风险等级")
    last_update_date = Column(Date, comment="最后更新日期")
    create_time = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    update_time = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")