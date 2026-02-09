#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库初始化脚本
用于执行DDL创建表结构和初始数据，详细输出每一步执行结果
"""

import os
import sys
from pathlib import Path
import psycopg2
from app.core.config import settings

def execute_sql_step_by_step():
    """逐行执行SQL语句并输出结果"""
    print("\n🔍 开始逐行执行SQL语句...")
    
    try:
        # 读取DDL文件
        with open('database_ddl.sql', 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        # 处理数据库URL格式（兼容SQLAlchemy格式）
        db_url = settings.DATABASE_URL
        if db_url.startswith('postgresql+psycopg2://'):
            # 转换为psycopg2可以直接使用的格式
            db_url = db_url.replace('postgresql+psycopg2://', 'postgresql://')
            print(f"🔧 自动转换数据库URL格式")
        
        # 连接数据库
        print("🔌 连接数据库...")
        print(f"🔗 连接字符串: {db_url}")
        conn = psycopg2.connect(db_url)
        conn.autocommit = False  # 关闭自动提交，便于回滚
        cursor = conn.cursor()
        print("✅ 数据库连接成功！")
        
        # 按分号分割SQL语句
        sql_statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip()]
        
        print(f"📝 共计 {len(sql_statements)} 条SQL语句需要执行\n")
        
        success_count = 0
        failed_statements = []
        
        # 逐条执行SQL语句
        for i, statement in enumerate(sql_statements, 1):
            try:
                # 提取语句的第一行作为标识
                first_line = statement.split('\n')[0].strip()
                if first_line.startswith('--'):
                    first_line = statement.split('\n')[1].strip() if len(statement.split('\n')) > 1 else first_line
                
                print(f"[{i}/{len(sql_statements)}] 执行: {first_line[:50]}{'...' if len(first_line) > 50 else ''}")
                
                cursor.execute(statement)
                conn.commit()
                print(f"    ✓ 执行成功")
                success_count += 1
                
            except Exception as e:
                conn.rollback()  # 回滚当前语句
                error_msg = str(e)
                print(f"    ✗ 执行失败: {error_msg}")
                failed_statements.append({
                    'index': i,
                    'statement': first_line[:100],
                    'error': error_msg
                })
                
                # 对于DROP语句失败，通常是可以接受的
                if 'DROP' in statement.upper() and 'does not exist' in error_msg.lower():
                    print(f"    ℹ️  表不存在，跳过DROP操作")
                    success_count += 1
                
                # 对于触发器函数相关的错误，提供特殊处理建议
                elif 'unterminated dollar-quoted string' in error_msg or 'syntax error at or near' in error_msg:
                    if 'update_updated_at_column' in statement:
                        print(f"    ⚠️  触发器函数语法错误，建议单独修复")
                        print(f"    💡 运行: python fix_triggers.py")
                        success_count += 1  # 让初始化继续进行
                
                continue
            
            # 每执行10条语句显示一次进度
            if i % 10 == 0:
                print(f"\n📊 进度: {i}/{len(sql_statements)} 条语句已完成 ({success_count} 成功, {len(failed_statements)} 失败)\n")
        
        # 关闭连接
        cursor.close()
        conn.close()
        
        # 输出最终结果
        print("\n" + "=" * 60)
        print("📊 执行结果统计:")
        print(f"   总语句数: {len(sql_statements)}")
        print(f"   成功执行: {success_count}")
        print(f"   执行失败: {len(failed_statements)}")
        print("=" * 60)
        
        if failed_statements:
            print("\n❌ 失败的语句详情:")
            for failed in failed_statements:
                print(f"   [{failed['index']}] {failed['statement']}...")
                print(f"       错误: {failed['error']}")
            return False
        else:
            print("\n✅ 所有SQL语句执行成功！")
            return True
            
    except FileNotFoundError:
        print("❌ 找不到 database_ddl.sql 文件")
        return False
    except Exception as e:
        print(f"❌ 数据库连接或执行出错: {str(e)}")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("工时与项目协同管理系统 - 数据库初始化 (详细模式)")
    print("=" * 60)
    
    try:
        # 检查数据库连接配置
        print(f"🗄️  数据库URL: {settings.DATABASE_URL}")
        
        # 逐行执行SQL语句
        success = execute_sql_step_by_step()
        
        if success:
            # 输出初始化信息
            print("\n" + "=" * 60)
            print("🎉 数据库初始化完成！")
            print("=" * 60)
            print("🔐 默认管理员账号:")
            print("   用户名: admin")
            print("   密码: admin123")
            print("\n💡 请根据实际需求修改初始数据和权限配置。")
        else:
            print("\n❌ 数据库初始化过程中出现错误，请查看上方详细信息")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n✗ 脚本执行出错: {str(e)}")
        print("请检查:")
        print("1. 数据库服务是否正常运行")
        print("2. DATABASE_URL配置是否正确")
        print("3. 是否有足够的数据库权限")
        sys.exit(1)

if __name__ == "__main__":
    main()
