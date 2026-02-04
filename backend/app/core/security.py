from datetime import datetime, timedelta
from typing import Any, Union
from passlib.context import CryptContext
from jose import jwt
from app.core.config import settings

# 密码加密上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# -------------------------- 密码操作 --------------------------
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码，捕获所有加密相关异常"""
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except (ValueError, RuntimeError):
        # 捕获bcrypt格式错误、长度超限、哈希非法等所有异常
        return False


def get_password_hash(password: str) -> str:
    """生成密码哈希，兜底异常处理"""
    try:
        return pwd_context.hash(password)
    except ValueError as e:
        # 适配bcrypt 72字节限制等硬性约束
        raise ValueError(f"密码格式非法：{str(e)}") from e


# -------------------------- JWT 操作 --------------------------
def create_access_token(subject: Union[str, Any], expires_delta: timedelta = None) -> str:
    """生成 JWT Token"""
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.JWT_EXPIRE_MINUTES)

    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm="HS256")
    return encoded_jwt