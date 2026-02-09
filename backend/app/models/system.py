from sqlalchemy import Column, Integer, String, DateTime, Text, SmallInteger, Boolean, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import JSONB
from app.models.base import Base
from datetime import datetime


class PermissionCode(Base):
    __tablename__ = "sys_permission_code"

    id = Column(Integer, primary_key=True, index=True, comment="权限码ID")
    code = Column(String(50), unique=True, nullable=False, comment="权限编码")
    name = Column(String(100), nullable=False, comment="权限名称")
    description = Column(Text, comment="权限描述")
    resource_type = Column(String(20), default="menu", comment="资源类型：menu-菜单，button-按钮，api-api接口")
    status = Column(SmallInteger, default=1, comment="状态：1-启用，0-禁用")
    create_time = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    update_time = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")


class Menu(Base):
    __tablename__ = "sys_menu"

    id = Column(Integer, primary_key=True, index=True, comment="菜单ID")
    pid = Column(Integer, ForeignKey("sys_menu.id"), comment="父级菜单ID")
    name = Column(String(100), nullable=False, comment="菜单名称")
    path = Column(String(200), comment="路由路径")
    component = Column(String(200), comment="组件路径")
    redirect = Column(String(200), comment="重定向路径")
    meta = Column(JSONB, comment="菜单元信息")
    icon = Column(String(50), comment="图标")
    type = Column(String(20), default="menu", comment="菜单类型：catalog-目录，menu-菜单，button-按钮，link-外链，embedded-内嵌")
    status = Column(SmallInteger, default=1, comment="状态：1-启用，0-禁用")
    sort_order = Column(Integer, default=0, comment="排序序号")
    auth_code = Column(String(50), comment="权限编码")
    create_time = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    update_time = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")


class UserRolePermission(Base):
    __tablename__ = "sys_user_role_permission"

    id = Column(Integer, primary_key=True, index=True, comment="用户角色权限ID")
    user_id = Column(Integer, ForeignKey("sys_user.id"), nullable=False, comment="用户ID")
    role_code = Column(String(50), nullable=False, comment="角色编码")
    permission_codes = Column(JSONB, comment="权限编码列表")
    create_time = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    update_time = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")


class TimeZone(Base):
    __tablename__ = "sys_timezone"

    id = Column(Integer, primary_key=True, index=True, comment="时区ID")
    timezone = Column(String(50), unique=True, nullable=False, comment="时区标识")
    offset = Column(Integer, nullable=False, comment="时区偏移（小时）")
    display_name = Column(String(100), comment="显示名称")
    country_code = Column(String(10), comment="国家代码")
    status = Column(SmallInteger, default=1, comment="状态：1-启用，0-禁用")
    create_time = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    update_time = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")