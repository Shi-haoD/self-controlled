#!/usr/bin/env python3
"""
前端Mock数据导入脚本
将Vben Admin的mock数据导入到后端数据库
"""

from app.core.database import get_db
from app.models.user import User, Role
from app.models.department import Department
from app.models.system import PermissionCode, Menu, UserRolePermission, TimeZone
from app.core.security import get_password_hash

# 前端mock数据
MOCK_USERS = [
    {
        'id': 0,
        'password': '123456',
        'realName': 'Vben',
        'roles': ['super'],
        'username': 'vben',
    },
    {
        'id': 1,
        'password': '123456',
        'realName': 'Admin',
        'roles': ['admin'],
        'username': 'admin',
        'homePath': '/workspace',
    },
    {
        'id': 2,
        'password': '123456',
        'realName': 'Jack',
        'roles': ['user'],
        'username': 'jack',
        'homePath': '/analytics',
    },
]

MOCK_CODES = [
    # super
    {
        'codes': ['AC_100100', 'AC_100110', 'AC_100120', 'AC_100010'],
        'username': 'vben',
    },
    # admin
    {
        'codes': ['AC_100010', 'AC_100020', 'AC_100030'],
        'username': 'admin',
    },
    # user
    {
        'codes': ['AC_1000001', 'AC_1000002'],
        'username': 'jack',
    },
]

MOCK_MENU_LIST = [
    {
        'id': 1,
        'name': 'Workspace',
        'status': 1,
        'type': 'menu',
        'icon': 'mdi:dashboard',
        'path': '/workspace',
        'component': '/dashboard/workspace/index',
        'meta': {
            'icon': 'carbon:workspace',
            'title': 'page.dashboard.workspace',
            'affixTab': True,
            'order': 0,
        },
    },
    {
        'id': 2,
        'meta': {
            'icon': 'carbon:settings',
            'order': 9997,
            'title': 'system.title',
            'badge': 'new',
            'badgeType': 'normal',
            'badgeVariants': 'primary',
        },
        'status': 1,
        'type': 'catalog',
        'name': 'System',
        'path': '/system',
        'children': [
            {
                'id': 201,
                'pid': 2,
                'path': '/system/menu',
                'name': 'SystemMenu',
                'authCode': 'System:Menu:List',
                'status': 1,
                'type': 'menu',
                'meta': {
                    'icon': 'carbon:menu',
                    'title': 'system.menu.title',
                },
                'component': '/system/menu/list',
                'children': [
                    {
                        'id': 20101,
                        'pid': 201,
                        'name': 'SystemMenuCreate',
                        'status': 1,
                        'type': 'button',
                        'authCode': 'System:Menu:Create',
                        'meta': {'title': 'common.create'},
                    },
                    {
                        'id': 20102,
                        'pid': 201,
                        'name': 'SystemMenuEdit',
                        'status': 1,
                        'type': 'button',
                        'authCode': 'System:Menu:Edit',
                        'meta': {'title': 'common.edit'},
                    },
                    {
                        'id': 20103,
                        'pid': 201,
                        'name': 'SystemMenuDelete',
                        'status': 1,
                        'type': 'button',
                        'authCode': 'System:Menu:Delete',
                        'meta': {'title': 'common.delete'},
                    },
                ],
            },
            {
                'id': 202,
                'pid': 2,
                'path': '/system/dept',
                'name': 'SystemDept',
                'status': 1,
                'type': 'menu',
                'authCode': 'System:Dept:List',
                'meta': {
                    'icon': 'carbon:container-services',
                    'title': 'system.dept.title',
                },
                'component': '/system/dept/list',
                'children': [
                    {
                        'id': 20401,
                        'pid': 202,
                        'name': 'SystemDeptCreate',
                        'status': 1,
                        'type': 'button',
                        'authCode': 'System:Dept:Create',
                        'meta': {'title': 'common.create'},
                    },
                    {
                        'id': 20402,
                        'pid': 202,
                        'name': 'SystemDeptEdit',
                        'status': 1,
                        'type': 'button',
                        'authCode': 'System:Dept:Edit',
                        'meta': {'title': 'common.edit'},
                    },
                    {
                        'id': 20403,
                        'pid': 202,
                        'name': 'SystemDeptDelete',
                        'status': 1,
                        'type': 'button',
                        'authCode': 'System:Dept:Delete',
                        'meta': {'title': 'common.delete'},
                    },
                ],
            },
        ],
    },
    {
        'id': 9,
        'meta': {
            'badgeType': 'dot',
            'order': 9998,
            'title': 'demos.vben.title',
            'icon': 'carbon:data-center',
        },
        'name': 'Project',
        'path': '/vben-admin',
        'type': 'catalog',
        'status': 1,
        'children': [
            {
                'id': 901,
                'pid': 9,
                'name': 'VbenDocument',
                'path': '/vben-admin/document',
                'component': 'IFrameView',
                'type': 'embedded',
                'status': 1,
                'meta': {
                    'icon': 'carbon:book',
                    'iframeSrc': 'https://doc.vben.pro',
                    'title': 'demos.vben.document',
                },
            },
            {
                'id': 902,
                'pid': 9,
                'name': 'VbenGithub',
                'path': '/vben-admin/github',
                'component': 'IFrameView',
                'type': 'link',
                'status': 1,
                'meta': {
                    'icon': 'carbon:logo-github',
                    'link': 'https://github.com/vbenjs/vue-vben-admin',
                    'title': 'Github',
                },
            },
            {
                'id': 903,
                'pid': 9,
                'name': 'VbenAntdv',
                'path': '/vben-admin/antdv',
                'component': 'IFrameView',
                'type': 'link',
                'status': 0,
                'meta': {
                    'icon': 'carbon:hexagon-vertical-solid',
                    'badgeType': 'dot',
                    'link': 'https://ant.vben.pro',
                    'title': 'demos.vben.antdv',
                },
            },
        ],
    },
    {
        'id': 10,
        'component': '_core/about/index',
        'type': 'menu',
        'status': 1,
        'meta': {
            'icon': 'lucide:copyright',
            'order': 9999,
            'title': 'demos.vben.about',
        },
        'name': 'About',
        'path': '/about',
    },
]

TIME_ZONE_OPTIONS = [
    {'offset': -5, 'timezone': 'America/New_York'},
    {'offset': 0, 'timezone': 'Europe/London'},
    {'offset': 8, 'timezone': 'Asia/Shanghai'},
    {'offset': 9, 'timezone': 'Asia/Tokyo'},
    {'offset': 9, 'timezone': 'Asia/Seoul'},
]

def import_mock_data():
    """导入前端mock数据"""
    print("=== 开始导入前端Mock数据 ===")
    
    try:
        db_gen = get_db()
        db = next(db_gen)
        
        # 1. 导入用户数据
        print("\n--- 导入用户数据 ---")
        for user_data in MOCK_USERS:
            # 检查用户是否已存在
            existing_user = db.query(User).filter(User.username == user_data['username']).first()
            if existing_user:
                print(f"  ✓ 用户 {user_data['username']} 已存在")
                continue
            
            # 创建新用户
            hashed_password = get_password_hash(user_data['password'])
            user = User(
                username=user_data['username'],
                password=hashed_password,
                real_name=user_data['realName'],
                email=f"{user_data['username']}@example.com",
                dept_id=1,  # 默认分配到技术部
                role_id=1 if 'super' in user_data['roles'] else (2 if 'admin' in user_data['roles'] else 6),
                status=1
            )
            db.add(user)
            print(f"  ✓ 创建用户: {user_data['realName']} ({user_data['username']})")
        
        db.flush()
        
        # 2. 导入权限码数据
        print("\n--- 导入权限码数据 ---")
        all_codes = set()
        for code_data in MOCK_CODES:
            all_codes.update(code_data['codes'])
        
        permission_descriptions = {
            'AC_100100': '超级权限1',
            'AC_100110': '超级权限2', 
            'AC_100120': '超级权限3',
            'AC_100010': '基础权限',
            'AC_100020': '管理权限1',
            'AC_100030': '管理权限2',
            'AC_1000001': '用户权限1',
            'AC_1000002': '用户权限2',
            'System:Menu:List': '菜单列表',
            'System:Menu:Create': '创建菜单',
            'System:Menu:Edit': '编辑菜单',
            'System:Menu:Delete': '删除菜单',
            'System:Dept:List': '部门列表',
            'System:Dept:Create': '创建部门',
            'System:Dept:Edit': '编辑部门',
            'System:Dept:Delete': '删除部门',
        }
        
        for code in all_codes:
            existing = db.query(PermissionCode).filter(PermissionCode.code == code).first()
            if existing:
                print(f"  ✓ 权限码 {code} 已存在")
                continue
            
            perm = PermissionCode(
                code=code,
                name=permission_descriptions.get(code, f'权限-{code}'),
                description=f'前端mock权限码 {code}',
                resource_type='menu' if ':' not in code else 'button',
                status=1
            )
            db.add(perm)
            print(f"  ✓ 创建权限码: {code}")
        
        db.flush()
        
        # 3. 导入用户角色权限关联
        print("\n--- 导入用户角色权限关联 ---")
        for code_data in MOCK_CODES:
            user = db.query(User).filter(User.username == code_data['username']).first()
            if not user:
                print(f"  ✗ 未找到用户 {code_data['username']}")
                continue
            
            # 获取用户角色
            role_map = {'vben': 'super', 'admin': 'admin', 'jack': 'user'}
            role_code = role_map.get(code_data['username'], 'user')
            
            # 创建用户角色权限关联
            user_perm = UserRolePermission(
                user_id=user.id,
                role_code=role_code,
                permission_codes=code_data['codes']
            )
            db.add(user_perm)
            print(f"  ✓ 为用户 {code_data['username']} 分配 {len(code_data['codes'])} 个权限")
        
        # 4. 导入菜单数据
        print("\n--- 导入菜单数据 ---")
        def create_menu_recursive(menu_data, parent_id=None):
            menu = Menu(
                id=menu_data['id'],
                pid=parent_id,
                name=menu_data['name'],
                path=menu_data.get('path'),
                component=menu_data.get('component'),
                redirect=menu_data.get('redirect'),
                meta=menu_data.get('meta'),
                icon=menu_data.get('icon'),
                type=menu_data['type'],
                status=menu_data['status'],
                auth_code=menu_data.get('authCode'),
                sort_order=menu_data.get('meta', {}).get('order', 0) if isinstance(menu_data.get('meta'), dict) else 0
            )
            db.add(menu)
            print(f"  ✓ 创建菜单: {menu_data['name']} (ID: {menu_data['id']})")
            
            # 递归创建子菜单
            if 'children' in menu_data:
                for child in menu_data['children']:
                    create_menu_recursive(child, menu_data['id'])
        
        for menu_item in MOCK_MENU_LIST:
            create_menu_recursive(menu_item)
        
        # 5. 导入时区数据
        print("\n--- 导入时区数据 ---")
        for tz_data in TIME_ZONE_OPTIONS:
            existing = db.query(TimeZone).filter(TimeZone.timezone == tz_data['timezone']).first()
            if existing:
                print(f"  ✓ 时区 {tz_data['timezone']} 已存在")
                continue
            
            tz = TimeZone(
                timezone=tz_data['timezone'],
                offset=tz_data['offset'],
                display_name=f"{tz_data['timezone']} (UTC{tz_data['offset']:+d})",
                country_code='US' if 'America' in tz_data['timezone'] else ('GB' if 'Europe' in tz_data['timezone'] else 'CN')
            )
            db.add(tz)
            print(f"  ✓ 创建时区: {tz_data['timezone']} (UTC{tz_data['offset']:+d})")
        
        db.commit()
        print("\n✓ Mock数据导入完成")
        
        # 验证导入结果
        print("\n--- 导入结果验证 ---")
        user_count = db.query(User).count()
        perm_count = db.query(PermissionCode).count()
        menu_count = db.query(Menu).count()
        tz_count = db.query(TimeZone).count()
        print(f"  用户总数: {user_count}")
        print(f"  权限码总数: {perm_count}")
        print(f"  菜单总数: {menu_count}")
        print(f"  时区总数: {tz_count}")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"✗ 数据导入失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    import_mock_data()