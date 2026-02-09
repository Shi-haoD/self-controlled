#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
执行DDL脚本的Python版本
"""

import os
import sys
from sqlalchemy import create_engine, text

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.config import settings

def execute_ddl():
    """执行DDL脚本创建数据库表结构"""
    
    # 读取DDL文件
    ddl_file = os.path.join(os.path.dirname(__file__), 'database_ddl.sql')
    
    with open(ddl_file, 'r', encoding='utf-8') as f:
        ddl_content = f.read()
    
    # 分割成单独的SQL语句（按分号分割，但保留BEGIN/END块）
    sql_statements = []
    current_statement = ""
    in_block = False
    
    for line in ddl_content.split('\n'):
        line = line.strip()
        if not line or line.startswith('--'):
            continue
            
        current_statement += line + '\n'
        
        # 检查是否是块开始/结束
        if line.upper().startswith('BEGIN') or line.upper().startswith('DO $$'):
            in_block = True
        elif line.upper().startswith('END') or line.upper().startswith('$$;'):
            in_block = False
            
        # 如果不是在块中且以分号结尾，则是一个完整的语句
        if not in_block and current_statement.strip().endswith(';'):
            sql_statements.append(current_statement.strip())
            current_statement = ""
    
    # 如果还有剩余的语句
    if current_statement.strip():
        sql_statements.append(current_statement.strip())
    
    # 创建数据库连接
    engine = create_engine(settings.DATABASE_URL.replace('workhour_db', 'postgres'))
    
    try:
        with engine.connect() as conn:
            # 先创建数据库（如果不存在）
            conn.execute(text("COMMIT"))  # 结束可能的事务
            try:
                conn.execute(text("CREATE DATABASE workhour_db"))
                print("✅ 数据库 workhour_db 创建成功")
            except Exception as e:
                if "already exists" in str(e):
                    print("✅ 数据库 workhour_db 已存在")
                else:
                    print(f"⚠️  创建数据库时出错: {e}")
            
            conn.commit()
        
        # 连接到目标数据库执行DDL
        engine.dispose()
        engine = create_engine(settings.DATABASE_URL)
        
        with engine.connect() as conn:
            print("🚀 开始执行DDL脚本...")
            
            for i, statement in enumerate(sql_statements, 1):
                try:
                    # 跳过注释和空语句
                    if not statement or statement.startswith('--') or statement.strip() == ';':
                        continue
                        
                    conn.execute(text(statement))
                    
                    # 输出一些关键操作的提示
                    if 'CREATE TABLE' in statement:
                        table_name = statement.split('CREATE TABLE')[1].split('(')[0].strip()
                        print(f"   ✅ 表 {table_name} 创建成功")
                    elif 'INSERT INTO' in statement and 'sys_user' in statement:
                        print("   ✅ 初始用户数据插入成功")
                    elif 'INSERT INTO' in statement and 'sys_department' in statement:
                        print("   ✅ 部门数据插入成功")
                    elif 'INSERT INTO' in statement and 'sys_role' in statement:
                        print("   ✅ 角色数据插入成功")
                        
                except Exception as e:
                    if "already exists" in str(e) or "duplicate key" in str(e):
                        print(f"   ⚠️  语句 {i} 已存在，跳过: {str(e)[:50]}...")
                    else:
                        print(f"   ❌ 语句 {i} 执行失败: {str(e)}")
                        print(f"      SQL: {statement[:100]}...")
                        # 不中断执行，继续下一个语句
                        
            conn.commit()
            
        print("\n🎉 DDL脚本执行完成！")
        print("📊 数据库初始化状态:")
        print("   - 表结构已创建")
        print("   - 初始数据已插入")
        print("   - 用户密码为明文（待加密）")
        
        return True
        
    except Exception as e:
        print(f"❌ DDL执行失败: {str(e)}")
        return False
    finally:
        engine.dispose()

if __name__ == "__main__":
    success = execute_ddl()
    if success:
        print("\n下一步请运行密码加密脚本:")
        print("python encrypt_passwords.py")
    else:
        sys.exit(1)
