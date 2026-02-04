from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.deps import get_db, get_current_user
from app.models.user import User
from app.schemas.user import UserInfoResponse
from app.utils.response import success_response

router = APIRouter()

# 获取当前登录用户信息：适配 Vben 要求字段
@router.get("/info",summary="获取当前登录用户信息")
def get_user_info(current_user: User = Depends(get_current_user)):
    data = UserInfoResponse(
        realName=current_user.real_name,
        roles=[current_user.role]
    ).model_dump()
    return success_response(data=data, message="获取用户信息成功")