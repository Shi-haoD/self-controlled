#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
密码加密脚本
用于将数据库中明文密码转换为bcrypt加密格式
"""

import os
import sys
from sqlalchemy import create_engine, text
import bcrypt

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.config import settings

def encrypt_user_passwords():
    """加密所有用户的密码"""
    # 创建数据库连接
    engine = create_engine(settings.DATABASE_URL)
    
    try:
        with engine.connect() as conn:
            # 查询所有密码为明文的用户（假设明文密码不含$符号）
            result = conn.execute(text("""
                SELECT id, username, password 
                FROM sys_user 
                WHERE password NOT LIKE '$2b$%'
            """))
            
            users_to_encrypt = result.fetchall()
            
            if not users_to_encrypt:
                print("✅ 所有用户密码已经是加密状态")
                return
            
            print(f"🔍 发现 {len(users_to_encrypt)} 个需要加密的用户")
            
            # 加密每个用户的密码
            for user in users_to_encrypt:
                user_id, username, plain_password = user
                
                # 生成bcrypt哈希
                hashed_password = bcrypt.hashpw(
                    plain_password.encode('utf-8'), 
                    bcrypt.gensalt()
                ).decode('utf-8')
                
                # 更新数据库中的密码
                conn.execute(text("""
                    UPDATE sys_user 
                    SET password = :hashed_password 
                    WHERE id = :user_id
                """), {
                    'hashed_password': hashed_password,
                    'user_id': user_id
                })
                
                print(f"✅ 用户 '{username}' 密码已加密")
            
            # 提交事务
            conn.commit()
            print(f"\n🎉 成功加密 {len(users_to_encrypt)} 个用户密码")
            
    except Exception as e:
        print(f"❌ 密码加密失败: {str(e)}")
        raise
    finally:
        engine.dispose()

def verify_encryption():
    """验证密码加密结果"""
    engine = create_engine(settings.DATABASE_URL)
    
    try:
        with engine.connect() as conn:
            # 统计加密和未加密的用户数量
            result = conn.execute(text("""
                SELECT 
                    COUNT(*) as total_users,
                    COUNT(CASE WHEN password LIKE '$2b$%' THEN 1 END) as encrypted_users,
                    COUNT(CASE WHEN password NOT LIKE '$2b$%' THEN 1 END) as plain_users
                FROM sys_user
            """))
            
            stats = result.fetchone()
            total, encrypted, plain = stats
            
            print(f"\n📊 密码加密状态统计:")
            print(f"   总用户数: {total}")
            print(f"   已加密用户: {encrypted}")
            print(f"   明文用户: {plain}")
            
            if plain > 0:
                print(f"\n⚠️  仍有 {plain} 个用户的密码未加密:")
                plain_users = conn.execute(text("""
                    SELECT username, password 
                    FROM sys_user 
                    WHERE password NOT LIKE '$2b$%'
                """)).fetchall()
                
                for user in plain_users:
                    print(f"   - {user[0]}: {user[1]}")
            
            return plain == 0
            
    except Exception as e:
        print(f"❌ 验证失败: {str(e)}")
        return False
    finally:
        engine.dispose()

if __name__ == "__main__":
    print("🔐 开始密码加密过程...")
    
    try:
        # 加密密码
        encrypt_user_passwords()
        
        # 验证结果
        success = verify_encryption()
        
        if success:
            print("\n✅ 所有密码均已成功加密！")
            print("📝 默认登录账号:")
            print("   admin / admin123")
            print("   zhangsan / zhangsan123")
            print("   lisi / lisi123")
            print("   wangwu / wangwu123")
            print("   zhaoliu / zhaoliu123")
            print("   sunqi / sunqi123")
        else:
            print("\n❌ 密码加密未完全成功，请检查上述警告信息")
            
    except Exception as e:
        print(f"\n💥 执行过程中发生错误: {str(e)}")
        sys.exit(1)
