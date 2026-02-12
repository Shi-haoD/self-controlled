#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
手动插入测试用户数据
"""

import os
import sys
from sqlalchemy import create_engine, text

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.config import settings

def insert_test_users():
    """插入测试用户"""
    users_data = [
        ('zhangsan', 'zhangsan123', '张三', 'zhangsan@example.com', 1, 2),
        ('lisi', 'lisi123', '李四', 'lisi@example.com', 1, 3),
        ('wangwu', 'wangwu123', '王五', 'wangwu@example.com', 2, 4),
        ('zhaoliu', 'zhaoliu123', '赵六', 'zhaoliu@example.com', 3, 5),
        ('sunqi', 'sunqi123', '孙七', 'sunqi@example.com', 1, 6),
    ]
    
    engine = create_engine(settings.DATABASE_URL)
    
    try:
        with engine.connect() as conn:
            print("开始插入测试用户...")
            
            for username, password, real_name, email, dept_id, role_id in users_data:
                try:
                    conn.execute(text("""
                        INSERT INTO sys_user (username, password, real_name, email, dept_id, role_id, status)
                        VALUES (:username, :password, :real_name, :email, :dept_id, :role_id, 1)
                    """), {
                        'username': username,
                        'password': password,  # 明文密码
                        'real_name': real_name,
                        'email': email,
                        'dept_id': dept_id,
                        'role_id': role_id
                    })
                    print(f"  ✅ 用户 {username} 插入成功")
                except Exception as e:
                    if "duplicate key" in str(e):
                        print(f"  ⚠️  用户 {username} 已存在")
                    else:
                        print(f"  ❌ 用户 {username} 插入失败: {e}")
            
            conn.commit()
            print("✅ 用户插入完成")
            
    except Exception as e:
        print(f"❌ 插入失败: {str(e)}")
    finally:
        engine.dispose()

if __name__ == "__main__":
    insert_test_users()
