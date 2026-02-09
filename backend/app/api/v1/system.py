from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.deps import get_db, get_current_user
from app.models.user import User
from app.models.system import PermissionCode, Menu, UserRolePermission, TimeZone
from app.utils.response import success_response, fail_response
from typing import List, Optional

router = APIRouter()

# 权限码相关接口

@router.get("/codes", summary="获取用户权限码")
def get_user_codes(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    获取当前登录用户的权限码列表
    """
    try:
        # 查询用户的角色权限
        user_perms = db.query(UserRolePermission).filter(
            UserRolePermission.user_id == current_user.id
        ).first()
        
        if user_perms:
            codes = user_perms.permission_codes or []
        else:
            codes = []
        
        return success_response(data=codes, message="获取权限码成功")
    except Exception as e:
        return fail_response(message=f"获取权限码失败: {str(e)}", code=5001)

@router.get("/codes/all", summary="获取所有权限码")
def get_all_codes(db: Session = Depends(get_db)):
    """
    获取系统所有权限码（管理员接口）
    """
    try:
        codes = db.query(PermissionCode).filter(PermissionCode.status == 1).all()
        result = [
            {
                "code": code.code,
                "name": code.name,
                "description": code.description,
                "resourceType": code.resource_type
            }
            for code in codes
        ]
        return success_response(data=result, message="获取权限码列表成功")
    except Exception as e:
        return fail_response(message=f"获取权限码列表失败: {str(e)}", code=5002)

# 菜单相关接口

@router.get("/menus", summary="获取用户菜单")
def get_user_menus(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    获取当前用户有权访问的菜单列表
    """
    try:
        # 查询用户的角色权限
        user_perms = db.query(UserRolePermission).filter(
            UserRolePermission.user_id == current_user.id
        ).first()
        
        if not user_perms:
            return success_response(data=[], message="用户无菜单权限")
        
        # 获取用户权限码
        user_codes = set(user_perms.permission_codes or [])
        
        # 查询所有启用的菜单
        all_menus = db.query(Menu).filter(Menu.status == 1).order_by(Menu.sort_order).all()
        
        # 过滤用户有权访问的菜单
        def filter_menu_by_permissions(menu):
            # 如果菜单没有指定权限码，则默认可见
            if not menu.auth_code:
                return True
            # 检查用户是否拥有该菜单的权限
            return menu.auth_code in user_codes
        
        # 构建菜单树
        def build_menu_tree(menus, parent_id=None):
            result = []
            for menu in menus:
                if menu.pid == parent_id and filter_menu_by_permissions(menu):
                    menu_dict = {
                        "id": menu.id,
                        "name": menu.name,
                        "path": menu.path,
                        "component": menu.component,
                        "redirect": menu.redirect,
                        "meta": menu.meta,
                        "icon": menu.icon,
                        "type": menu.type
                    }
                    # 递归处理子菜单
                    children = build_menu_tree(menus, menu.id)
                    if children:
                        menu_dict["children"] = children
                    result.append(menu_dict)
            return result
        
        menu_tree = build_menu_tree(all_menus)
        return success_response(data=menu_tree, message="获取菜单成功")
    except Exception as e:
        return fail_response(message=f"获取菜单失败: {str(e)}", code=5003)

@router.get("/menus/all", summary="获取所有菜单")
def get_all_menus(db: Session = Depends(get_db)):
    """
    获取系统所有菜单（管理员接口）
    """
    try:
        # 查询所有菜单
        all_menus = db.query(Menu).order_by(Menu.sort_order).all()
        
        # 构建菜单树
        def build_full_menu_tree(menus, parent_id=None):
            result = []
            for menu in menus:
                if menu.pid == parent_id:
                    menu_dict = {
                        "id": menu.id,
                        "pid": menu.pid,
                        "name": menu.name,
                        "path": menu.path,
                        "component": menu.component,
                        "redirect": menu.redirect,
                        "meta": menu.meta,
                        "icon": menu.icon,
                        "type": menu.type,
                        "status": menu.status,
                        "authCode": menu.auth_code,
                        "sortOrder": menu.sort_order
                    }
                    # 递归处理子菜单
                    children = build_full_menu_tree(menus, menu.id)
                    if children:
                        menu_dict["children"] = children
                    result.append(menu_dict)
            return result
        
        menu_tree = build_full_menu_tree(all_menus)
        return success_response(data=menu_tree, message="获取菜单列表成功")
    except Exception as e:
        return fail_response(message=f"获取菜单列表失败: {str(e)}", code=5004)

@router.get("/menus/list", summary="获取扁平化菜单列表")
def get_menu_list(db: Session = Depends(get_db)):
    """
    获取扁平化的菜单列表（用于表格展示）
    """
    try:
        menus = db.query(Menu).order_by(Menu.sort_order).all()
        result = [
            {
                "id": menu.id,
                "pid": menu.pid,
                "name": menu.name,
                "path": menu.path,
                "component": menu.component,
                "type": menu.type,
                "status": menu.status,
                "authCode": menu.auth_code,
                "sortOrder": menu.sort_order
            }
            for menu in menus
        ]
        return success_response(data=result, message="获取菜单列表成功")
    except Exception as e:
        return fail_response(message=f"获取菜单列表失败: {str(e)}", code=5005)

# 时区相关接口

@router.get("/timezones", summary="获取时区列表")
def get_timezones(db: Session = Depends(get_db)):
    """
    获取系统支持的时区列表
    """
    try:
        timezones = db.query(TimeZone).filter(TimeZone.status == 1).all()
        result = [
            {
                "id": tz.id,
                "timezone": tz.timezone,
                "offset": tz.offset,
                "displayName": tz.display_name,
                "countryCode": tz.country_code
            }
            for tz in timezones
        ]
        return success_response(data=result, message="获取时区列表成功")
    except Exception as e:
        return fail_response(message=f"获取时区列表失败: {str(e)}", code=5006)

@router.get("/timezones/options", summary="获取时区选项")
def get_timezone_options(db: Session = Depends(get_db)):
    """
    获取时区选项（用于前端选择器）
    """
    try:
        timezones = db.query(TimeZone).filter(TimeZone.status == 1).all()
        result = [
            {
                "value": tz.timezone,
                "label": f"{tz.display_name} (UTC{tz.offset:+d})"
            }
            for tz in timezones
        ]
        return success_response(data=result, message="获取时区选项成功")
    except Exception as e:
        return fail_response(message=f"获取时区选项失败: {str(e)}", code=5007)