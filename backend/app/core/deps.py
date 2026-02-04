from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.config import settings
from app.crud.user import user_crud

# OAuth2 认证规则，对应前端 Bearer Token 传递方式
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_current_user(
        db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
):
    """
    依赖项：解析 Token，获取当前登录用户
    所有需要登录权限的接口，都依赖此函数
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无效的认证凭证，请重新登录",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # 查询数据库用户
    user = user_crud.get(db, id=int(user_id))
    if user is None:
        raise credentials_exception
    return user