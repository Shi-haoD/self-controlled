from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.deps import get_db, get_current_user
from app.models.user import User
from app.utils.response import success_response, fail_response
from typing import List, Optional

router = APIRouter()

# 菜单数据结构定义
class RouteRecordStringComponent:
    def __init__(self, path: str, component: str, meta: dict, children: Optional[List] = None):
        self.path = path
        self.component = component
        self.meta = meta
        self.children = children or []

# 模拟菜单数据 - 实际项目中应该从数据库获取
MOCK_MENUS = [
    RouteRecordStringComponent(
        path="/dashboard",
        component="/dashboard/index.vue",
        meta={"title": "仪表板", "icon": "dashboard"}
    ),
    RouteRecordStringComponent(
        path="/worklog",
        component="/worklog/index.vue",
        meta={"title": "工作日志", "icon": "document"}
    ),
    RouteRecordStringComponent(
        path="/project",
        component="/project/index.vue",
        meta={"title": "项目管理", "icon": "folder"}
    ),
    RouteRecordStringComponent(
        path="/plan",
        component="/plan/index.vue",
        meta={"title": "计划管理", "icon": "calendar"}
    ),
    RouteRecordStringComponent(
        path="/report",
        component="/report/index.vue",
        meta={"title": "报表统计", "icon": "pie-chart"}
    )
]

@router.get("/all", summary="获取用户所有菜单")
def get_all_menus(current_user: User = Depends(get_current_user)):
    """
    获取当前用户的菜单权限列表
    """
    try:
        # 这里可以根据用户角色返回不同的菜单
        # 简单实现：返回所有菜单
        menus_data = []
        for menu in MOCK_MENUS:
            menu_dict = {
                "path": menu.path,
                "component": menu.component,
                "meta": menu.meta
            }
            if menu.children:
                menu_dict["children"] = menu.children
            menus_data.append(menu_dict)
        
        return success_response(data=menus_data, message="获取菜单成功")
    except Exception as e:
        return fail_response(message=f"获取菜单失败: {str(e)}", code=5001)