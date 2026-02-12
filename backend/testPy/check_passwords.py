#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查数据库中用户密码状态
"""

import os
import sys
from sqlalchemy import create_engine, text

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.config import settings

def check_user_passwords():
    """检查用户密码状态"""
    engine = create_engine(settings.DATABASE_URL)
    
    try:
        with engine.connect() as conn:
            # 查询所有用户及其密码
            result = conn.execute(text("""
                SELECT id, username, password, real_name
                FROM sys_user
                ORDER BY id
            """))
            
            users = result.fetchall()
            
            print("📋 用户密码状态检查:")
            print("-" * 50)
            
            for user in users:
                user_id, username, password, real_name = user
                is_encrypted = password.startswith('$2b$')
                status = "🔒 已加密" if is_encrypted else "🔓 明文"
                
                print(f"ID:{user_id:2d} | {username:12s} | {real_name:8s} | {status}")
                if not is_encrypted:
                    print(f"       明文密码: {password}")
            
            # 统计
            total = len(users)
            encrypted = sum(1 for u in users if u[2].startswith('$2b$'))
            plain = total - encrypted
            
            print("-" * 50)
            print(f"总计: {total} 用户 | 已加密: {encrypted} | 明文: {plain}")
            
            return plain == 0
            
    except Exception as e:
        print(f"❌ 检查失败: {str(e)}")
        return False
    finally:
        engine.dispose()

if __name__ == "__main__":
    all_encrypted = check_user_passwords()
    if all_encrypted:
        print("\n✅ 所有用户密码均已加密")
    else:
        print("\n⚠️  存在明文密码，需要重新加密")
