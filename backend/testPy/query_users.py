#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
查询用户数据
"""

import os
import sys
from sqlalchemy import create_engine, text

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.config import settings

def query_users():
    """查询所有用户"""
    engine = create_engine(settings.DATABASE_URL)
    
    try:
        with engine.connect() as conn:
            # 查询用户总数
            result = conn.execute(text("SELECT COUNT(*) FROM sys_user"))
            count = result.fetchone()[0]
            print(f"用户总数: {count}")
            
            # 查询所有用户
            result = conn.execute(text("SELECT username, real_name, password FROM sys_user ORDER BY id"))
            users = result.fetchall()
            
            print("\n所有用户:")
            for user in users:
                username, real_name, password = user
                is_encrypted = password.startswith('$2b$')
                print(f"  {username} ({real_name}) - {'已加密' if is_encrypted else '明文'}")
                if not is_encrypted:
                    print(f"    明文密码: {password}")
                    
    except Exception as e:
        print(f"查询失败: {str(e)}")
    finally:
        engine.dispose()

if __name__ == "__main__":
    query_users()
