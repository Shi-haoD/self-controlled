from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import sys
from app.api.v1 import auth, user
from app.models.base import Base
from app.core.database import engine
from app.utils.response import fail_response

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# 创建数据库表
Base.metadata.create_all(bind=engine)

# 初始化应用，关闭调试模式（生产环境必填）
app = FastAPI(
    title="Self Controlled Backend",
    version="0.1.0",
    debug=False  # 关闭调试，禁止暴露异常堆栈
)

# 跨域配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------- 全局异常处理器 --------------------------
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """统一拦截所有未捕获的异常，返回标准化响应"""
    logger.error(f"全局异常捕获: {str(exc)}", exc_info=True)
    # 返回规范格式，不暴露底层堆栈
    return JSONResponse(
        status_code=200,  # 接口层返回200，业务码标识错误
        content=fail_response(message="服务器异常，请稍后重试", code=5000)
    )

@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    """拦截参数校验类异常"""
    logger.warning(f"参数异常: {str(exc)}")
    return JSONResponse(
        status_code=200,
        content=fail_response(message=str(exc), code=4000)
    )

# 注册路由
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
# 如果user路由未实现，注释下一行即可
# app.include_router(user.router, prefix="/api/v1/user", tags=["User"])