from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.deps import get_db, get_current_user
from app.models.user import User
from app.utils.response import success_response, fail_response
from typing import List, Optional
import pytz

router = APIRouter()

# 时区相关接口

@router.get("/getTimezoneOptions", summary="获取系统支持的时区列表")
def get_timezone_options():
    """
    获取系统支持的所有时区选项
    """
    try:
        # 获取所有可用时区
        timezones = []
        for tz in pytz.all_timezones:
            # 只返回常用时区，可以根据需要筛选
            if '/' in tz:  # 过滤掉一些特殊时区
                timezones.append({
                    "label": tz.replace('_', ' '),
                    "value": tz
                })
        
        # 按地区分组排序
        timezones.sort(key=lambda x: x['value'])
        
        return success_response(data=timezones, message="获取时区列表成功")
    except Exception as e:
        return fail_response(message=f"获取时区列表失败: {str(e)}", code=5002)

@router.get("/getTimezone", summary="获取用户时区")
def get_user_timezone(current_user: User = Depends(get_current_user)):
    """
    获取当前用户的时区设置
    """
    try:
        # 从用户信息或其他配置中获取时区
        # 这里简单返回默认时区，实际项目中应该存储在用户表或配置表中
        user_timezone = getattr(current_user, 'timezone', 'Asia/Shanghai')
        return success_response(data=user_timezone, message="获取用户时区成功")
    except Exception as e:
        return fail_response(message=f"获取用户时区失败: {str(e)}", code=5003)

@router.post("/setTimezone", summary="设置用户时区")
def set_user_timezone(timezone_data: dict, current_user: User = Depends(get_current_user)):
    """
    设置用户的时区偏好
    """
    try:
        timezone = timezone_data.get('timezone')
        if not timezone:
            return fail_response(message="时区参数不能为空", code=4001)
        
        # 验证时区是否有效
        if timezone not in pytz.all_timezones:
            return fail_response(message="无效的时区", code=4002)
        
        # 这里应该更新数据库中的用户时区设置
        # 示例：current_user.timezone = timezone
        # db.commit()
        
        return success_response(message="时区设置成功")
    except Exception as e:
        return fail_response(message=f"设置时区失败: {str(e)}", code=5004)