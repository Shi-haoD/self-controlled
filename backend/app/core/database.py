from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from app.core.config import settings

# 创建引擎
engine = create_engine(settings.DATABASE_URL, echo=True)

# 创建会话工厂
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# 基础模型类
Base = declarative_base()

# 导入所有模型以确保它们被正确注册
from app.models.user import User, Role
from app.models.department import Department
from app.models.system import PermissionCode, Menu, UserRolePermission, TimeZone
from app.models.worklog import WorkDaily
from app.models.project import ProjectInfo, ProjectStatistic
from app.models.plan import AnnualPlan, WorkProblem
from app.models.notification import SysMessage, WorkTask
from app.models.report import ReportTemplate


def get_db():
    """数据库会话依赖"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """初始化数据库表结构"""
    Base.metadata.create_all(bind=engine)
