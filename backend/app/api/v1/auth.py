import logging
from datetime import timedelta
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.core.security import create_access_token
from app.crud.user import user_crud
from app.schemas.auth import (
    LoginRequest, LoginResponse,
    UserRegisterRequest, UserRegisterResponse
)
from app.utils.response import success_response, fail_response
from app.core.config import settings

# 初始化日志器（优化：记录用户操作日志）
logger = logging.getLogger(__name__)
router = APIRouter()

# 原有：登录接口
@router.post("/login", summary="用户登录")
def login(
    req: LoginRequest,
    db: Session = Depends(get_db)
):
    user = user_crud.authenticate(db, username=req.username, password=req.password)
    if not user:
        logger.warning(f"登录失败：用户名/密码错误 -> {req.username}")
        return fail_response(message="用户名或密码错误", code=1001)

    # 生成JWT令牌
    access_token = create_access_token(
        subject=user.id,
        expires_delta=timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
    )
    logger.info(f"登录成功：用户 -> {req.username}")
    return success_response(
        data=LoginResponse(accessToken=access_token).model_dump(),
        message="登录成功"
    )

# 优化集成：注册接口（权限控制+日志+参数校验）
# 优化集成：注册接口（权限控制+日志+参数校验）
@router.post("/register", summary="用户注册")
def register(
    req: UserRegisterRequest,
    db: Session = Depends(get_db)
):
    # 1. 核心权限控制：禁止通过公开注册接口创建管理员角色
    # if req.role != "user":
    #     logger.warning(f"非法注册请求：尝试创建管理员账号 -> {req.username}")
    #     return fail_response(message="仅允许注册普通用户，无法创建管理员", code=1003)

    # 2. 调用核心创建逻辑
    user = user_crud.create_user(db, obj_in=req)

    # 3. 判断创建结果：返回 None 代表注册失败（用户名重复/加密异常）
    if not user:
        logger.warning(f"注册失败：用户名已存在或密码加密异常 -> {req.username}")
        return fail_response(message="用户名已存在，注册失败", code=1002)

    # 4. 注册成功，构造响应数据
    resp_data = UserRegisterResponse(
        username=user.username,
        real_name=user.real_name,
        role=user.role
    ).model_dump()

    logger.info(f"注册成功：新用户 -> {req.username}")
    return success_response(
        data=resp_data,
        message="用户注册成功"
    )

# 原有：获取权限码接口
@router.get("/codes", summary="获取用户权限码")
def get_access_codes():
    return success_response(data=[], message="获取权限码成功")

# 原有：健康检查接口
@router.get("/ping", summary="服务连通性测试")
def ping():
    return success_response(message="pong")