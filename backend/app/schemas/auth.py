from pydantic import BaseModel, Field, field_validator
from typing import Optional
import re

# 登录请求参数（原有）
class LoginRequest(BaseModel):
    username: str
    password: str

# 登录返回 Token（原有）
class LoginResponse(BaseModel):
    accessToken: str

# 注册请求参数 + 全量校验
class UserRegisterRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=20, description="登录账号，3-20位字符")
    password: str = Field(..., min_length=6, max_length=100, description="登录密码")
    real_name: Optional[str] = Field(None, max_length=50, description="真实姓名")
    role: str = "user"

    # 校验1：必须包含字母+数字
    @field_validator('password')
    def validate_password_strength(cls, value: str) -> str:
        if not re.search(r'[A-Za-z]', value) or not re.search(r'[0-9]', value):
            raise ValueError('密码必须同时包含英文字母和数字')
        return value

    # 校验2：适配bcrypt限制，UTF8编码后≤72字节
    @field_validator('password')
    def validate_password_bytes(cls, value: str) -> str:
        byte_len = len(value.encode('utf-8'))
        if byte_len > 72:
            raise ValueError('密码过长，编码后长度不能超过72字节')
        return value

# 注册响应参数（原有）
class UserRegisterResponse(BaseModel):
    username: str
    real_name: str
    role: str