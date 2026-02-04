from pydantic import BaseModel
from typing import List

# 用户信息响应（适配 Vben UserInfo 字段）
class UserInfoResponse(BaseModel):
    realName: str  # 严格匹配前端要求
    roles: List[str]