from sqlalchemy import Column, Integer, String, Boolean
from app.models.base import Base


class User(Base):
    __tablename__ = "sys_user"  # 与之前数据库设计的表名一致

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, comment="登录账号")
    hashed_password = Column(String(255), comment="加密密码")
    real_name = Column(String(50), comment="真实姓名")
    role = Column(String(50), default="user", comment="角色标识")
    is_active = Column(Boolean, default=True, comment="账号状态")