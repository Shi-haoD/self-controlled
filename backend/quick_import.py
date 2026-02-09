#!/usr/bin/env python3
"""
简化版Mock数据导入脚本
"""

from app.core.database import get_db
from app.models.user import User
from app.models.system import PermissionCode, Menu, UserRolePermission, TimeZone
from app.core.security import get_password_hash

def quick_import():
    """快速导入基础数据"""
    print("开始导入基础数据...")
    
    try:
        db_gen = get_db()
        db = next(db_gen)
        
        # 导入基础用户
        users = [
            {'username': 'vben', 'password': '123456', 'real_name': 'Vben', 'role_id': 1},
            {'username': 'admin', 'password': '123456', 'real_name': 'Admin', 'role_id': 2},
            {'username': 'jack', 'password': '123456', 'real_name': 'Jack', 'role_id': 6}
        ]
        
        for user_data in users:
            existing = db.query(User).filter(User.username == user_data['username']).first()
            if not existing:
                user = User(
                    username=user_data['username'],
                    password=get_password_hash(user_data['password']),
                    real_name=user_data['real_name'],
                    email=f"{user_data['username']}@example.com",
                    dept_id=1,
                    role_id=user_data['role_id'],
                    status=1
                )
                db.add(user)
                print(f"创建用户: {user_data['username']}")
        
        # 导入基础权限码
        basic_codes = ['AC_100100', 'AC_100010', 'AC_100020', 'System:Menu:List']
        for code in basic_codes:
            existing = db.query(PermissionCode).filter(PermissionCode.code == code).first()
            if not existing:
                perm = PermissionCode(
                    code=code,
                    name=f'权限-{code}',
                    description=f'权限码 {code}',
                    resource_type='menu' if ':' not in code else 'button'
                )
                db.add(perm)
                print(f"创建权限码: {code}")
        
        db.commit()
        print("数据导入完成!")
        db.close()
        return True
        
    except Exception as e:
        print(f"导入失败: {e}")
        return False

if __name__ == "__main__":
    quick_import()