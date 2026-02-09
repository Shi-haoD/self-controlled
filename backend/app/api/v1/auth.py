import logging
from datetime import timedelta
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.deps import get_db, get_current_user
from app.core.security import create_access_token
from app.crud.user import user_crud
from app.schemas.auth import (
    LoginRequest, LoginResponse,
    UserRegisterRequest, UserRegisterResponse, RefreshTokenResponse
)
from app.utils.response import success_response, fail_response
from app.core.config import settings
from app.models.user import User

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
    print(user)
    # 3. 判断创建结果：返回 None 代表注册失败（用户名重复/加密异常）
    if not user:
        logger.warning(f"注册失败：用户名已存在或密码加密异常 -> {req.username}")
        return fail_response(message="用户名已存在，注册失败", code=1002)

    # 4. 注册成功，构造响应数据
    # 注意：数据库中没有role字段，使用固定值"user"
    resp_data = UserRegisterResponse(
        username=user.username,
        real_name=user.real_name,
        role="user"
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

# 新增：退出登录接口
@router.post("/logout", summary="用户退出登录")
def logout(current_user: User = Depends(get_current_user)):
    """
    用户退出登录
    在JWT模式下，主要是清除客户端token
    服务端可以记录登出日志
    """
    try:
        # 记录登出日志
        logger.info(f"用户退出登录: {current_user.username} (ID: {current_user.id})")
        
        # 在JWT模式下，服务端不需要特殊处理
        # 客户端负责清除本地存储的token
        return success_response(message="退出登录成功")
    except Exception as e:
        logger.error(f"退出登录异常: {str(e)}")
        return fail_response(message="退出登录失败", code=5005)

# 新增：临时密码重置接口（开发环境使用）
@router.post("/reset-admin-password", summary="重置管理员密码（开发用）")
def reset_admin_password_dev(db: Session = Depends(get_db)):
    """
    开发环境临时接口：重置管理员密码为admin123
    生产环境请勿使用此接口
    """
    try:
        from app.core.security import get_password_hash
        
        # 查找或创建管理员用户
        admin_user = db.query(User).filter(User.username == "admin").first()
        
        if not admin_user:
            # 创建新管理员
            hashed_password = get_password_hash("admin123")
            admin_user = User(
                username="admin",
                password=hashed_password,
                real_name="系统管理员",
                email="admin@example.com",
                role_id=1,
                status=1
            )
            db.add(admin_user)
            action = "创建"
        else:
            # 重置密码
            hashed_password = get_password_hash("admin123")
            admin_user.password = hashed_password
            action = "重置"
        
        db.commit()
        db.refresh(admin_user)
        
        logger.info(f"管理员密码已{action}: admin/admin123")
        return success_response(
            message=f"管理员密码已{action}为admin123，请立即修改"
        )
        
    except Exception as e:
        logger.error(f"重置管理员密码失败: {str(e)}")
        db.rollback()
        return fail_response(message="重置密码失败", code=5007)

# 新增：刷新token接口
@router.post("/refresh", summary="刷新访问令牌")
def refresh_token(current_user: User = Depends(get_current_user)):
    """
    刷新访问令牌
    使用当前有效的token换取新的token
    """
    try:
        # 生成新的JWT令牌
        new_access_token = create_access_token(
            subject=current_user.id,
            expires_delta=timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
        )
        
        logger.info(f"用户刷新token: {current_user.username} (ID: {current_user.id})")
        
        return success_response(
            data=RefreshTokenResponse(accessToken=new_access_token).model_dump(),
            message="token刷新成功"
        )
    except Exception as e:
        logger.error(f"刷新token异常: {str(e)}")
        return fail_response(message="token刷新失败", code=5006)