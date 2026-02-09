from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.deps import get_db, get_current_user
from app.models.user import User
from app.schemas.user import UserInfoResponse
from app.utils.response import success_response

router = APIRouter()

# 获取当前登录用户信息：适配 Vben 要求字段
@router.get("/info",summary="获取当前登录用户信息")
def get_user_info(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    print('current_user:', vars(current_user))
    
    # 根据role_id获取角色信息
    from app.models.user import Role
    role_info = "user"  # 默认角色
    
    if current_user.role_id:
        role = db.query(Role).filter(Role.id == current_user.role_id).first()
        if role:
            role_info = role.role_code or "user"
    
    data = UserInfoResponse(
        realName=current_user.real_name,
        roles=[role_info]
    ).model_dump()
    return success_response(data=data, message="获取用户信息成功")