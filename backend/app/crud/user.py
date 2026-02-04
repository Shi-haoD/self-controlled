from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import logging
from app.crud.base import BaseCRUD
from app.models.user import User
from app.core.security import verify_password, get_password_hash
from app.schemas.auth import UserRegisterRequest

# 新增日志器，用于调试
logger = logging.getLogger(__name__)

class UserCRUD(BaseCRUD[User]):
    def __init__(self):
        super().__init__(User)

    def authenticate(self, db: Session, *, username: str, password: str) -> Optional[User]:
        user = self.get_by_username(db, username=username)
        if not user:
            return None
        try:
            is_valid = verify_password(password, user.hashed_password)
        except (ValueError, RuntimeError):
            return None
        return user if is_valid else None

    def create_user(self, db: Session, *, obj_in: UserRegisterRequest) -> Optional[User]:
        # 1. 校验用户名：查询是否已存在
        user = self.get_by_username(db, username=obj_in.username)
        if user:
            # 关键调试日志：明确打印用户名重复
            logger.error(f"【调试】注册失败：用户名 {obj_in.username} 已存在于数据库")
            return None

        try:
            # 2. 尝试加密密码
            logger.info(f"【调试】开始加密用户 {obj_in.username} 的密码")
            hashed_pwd = get_password_hash(obj_in.password)
            logger.info(f"【调试】密码加密完成")
        except (ValueError, RuntimeError) as e:
            # 关键调试日志：打印加密异常详情
            logger.error(f"【调试】密码加密失败：{str(e)}", exc_info=True)
            return None

        # 构建数据库对象
        db_obj = User(
            username=obj_in.username,
            hashed_password=hashed_pwd,
            real_name=obj_in.real_name or obj_in.username,
            role=obj_in.role,
            is_active=True
        )

        try:
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            logger.info(f"【调试】用户 {obj_in.username} 写入数据库成功")
            return db_obj
        except IntegrityError:
            db.rollback()
            logger.error(f"【调试】数据库事务冲突，注册失败")
            return None

user_crud = UserCRUD()