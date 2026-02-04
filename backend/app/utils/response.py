from typing import Any, Optional
from pydantic import BaseModel


# 统一响应模型，贴合 Vben 前端规范
class BaseResponse(BaseModel):
    code: int = 0  # 0=成功，非0=失败
    data: Optional[Any] = None
    message: str = "操作成功"


# 成功响应（通用封装）
def success_response(data: Any = None, message: str = "操作成功") -> dict:
    return BaseResponse(code=0, data=data, message=message).model_dump()


# 失败响应（通用封装）
def fail_response(message: str = "操作失败", code: int = 1001) -> dict:
    return BaseResponse(code=code, data=None, message=message).model_dump()