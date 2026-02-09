from typing import Generator, Optional
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.config import settings
from app.crud.user import user_crud

# OAuth2 认证规则
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_current_user(
        request: Request, db: Session = Depends(get_db)
):
    """
    依赖项：解析 Token，获取当前登录用户
    支持两种格式：'Bearer token' 或直接 'token'
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无效的认证凭证，请重新登录",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # 从请求头中获取Authorization
    authorization: str = request.headers.get("Authorization")
    if not authorization:
        raise credentials_exception
    
    # 自动处理Bearer前缀
    token = authorization
    if authorization.startswith("Bearer "):
        token = authorization[7:]  # 移除"Bearer "前缀
    
    try:
        print(f"DEBUG: 接收的authorization头: {authorization}")
        print(f"DEBUG: 处理后的token: {token}")
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
        print(f"DEBUG: 解码成功的payload: {payload}")
        user_id: str = payload.get("sub")
        print(f"DEBUG: 提取的用户ID: {user_id}")
        if user_id is None:
            print("DEBUG: 用户ID为空")
            raise credentials_exception
    except JWTError as e:
        print(f"DEBUG: JWT解码失败: {str(e)}")
        raise credentials_exception

    # 查询数据库用户
    try:
        user_id_int = int(user_id)
        print(f"DEBUG: 转换后的用户ID: {user_id_int}")
        user = user_crud.get(db, id=user_id_int)
        print(f"DEBUG: 数据库查询结果: {user}")
        print(f"DEBUG: 用户是否存在: {user is not None}")
        if user is None:
            print("DEBUG: 数据库中未找到该用户")
            raise credentials_exception
        print(f"DEBUG: 返回用户对象: {user.username}")
        return user
    except Exception as e:
        print(f"DEBUG: 数据库查询异常: {str(e)}")
        raise credentials_exception