from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, SmallInteger, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from app.models.base import Base
from datetime import datetime


class User(Base):
    __tablename__ = "sys_user"

    id = Column(Integer, primary_key=True, index=True, comment="用户ID")
    username = Column(String(50), unique=True, index=True, nullable=False, comment="登录账号")
    password = Column(String(255), nullable=False, comment="加密密码")
    real_name = Column(String(50), nullable=False, comment="真实姓名")
    email = Column(String(100), unique=True, comment="邮箱地址")
    phone = Column(String(20), comment="手机号码")
    dept_id = Column(Integer, ForeignKey("sys_department.id"), comment="所属部门ID")
    position = Column(String(100), comment="职位")
    role_id = Column(Integer, ForeignKey("sys_role.id"), comment="角色ID")
    status = Column(SmallInteger, default=1, comment="账号状态：1-启用，0-禁用")
    last_login = Column(DateTime, comment="最后登录时间")
    create_time = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    update_time = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")


class Role(Base):
    __tablename__ = "sys_role"

    id = Column(Integer, primary_key=True, index=True, comment="角色ID")
    role_name = Column(String(50), nullable=False, comment="角色名称")
    role_code = Column(String(50), unique=True, nullable=False, comment="角色编码")
    role_desc = Column(Text, comment="角色描述")
    permissions = Column(JSONB, comment="权限配置JSON")
    data_scope = Column(String(20), default="personal", comment="数据权限范围")
    status = Column(SmallInteger, default=1, comment="角色状态：1-启用，0-禁用")
    create_time = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    update_time = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")