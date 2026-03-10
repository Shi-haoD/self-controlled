#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库初始化脚本
用于执行 DDL 创建表结构和初始数据，详细输出每一步执行结果
并在首次创建时自动加密用户密码
"""

import os
import sys
from pathlib import Path
# 🔥 修复1：统一使用新版 psycopg（删除psycopg2相关）
import psycopg
import bcrypt
from app.core.config import settings


def encrypt_user_passwords(conn):
    """加密所有用户的明文密码"""
    print("\n🔐 开始加密用户密码...")

    try:
        cursor = conn.cursor()

        # 查询所有密码为明文的用户（假设明文密码不含$符号）
        cursor.execute("""
                       SELECT id, username, password
                       FROM sys_user
                       WHERE password NOT LIKE '$2b$%'
                       """)

        users_to_encrypt = cursor.fetchall()

        if not users_to_encrypt:
            print("✅ 所有用户密码已经是加密状态")
            return True

        print(f"🔍 发现 {len(users_to_encrypt)} 个需要加密的用户")

        # 加密每个用户的密码
        for user in users_to_encrypt:
            user_id, username, plain_password = user

            # 生成 bcrypt 哈希
            hashed_password = bcrypt.hashpw(
                plain_password.encode('utf-8'),
                bcrypt.gensalt()
            ).decode('utf-8')

            # 更新数据库中的密码
            cursor.execute("""
                           UPDATE sys_user
                           SET password = %s
                           WHERE id = %s
                           """, (hashed_password, user_id))

            print(f"✅ 用户 '{username}' 密码已加密")

        # 提交事务
        conn.commit()
        print(f"\n🎉 成功加密 {len(users_to_encrypt)} 个用户密码")
        return True

    except Exception as e:
        print(f"❌ 密码加密失败：{str(e)}")
        return False
    finally:
        cursor.close()


def verify_encryption(conn):
    """验证密码加密结果"""
    print("\n📊 验证密码加密状态...")

    try:
        cursor = conn.cursor()

        # 统计加密和未加密的用户数量
        cursor.execute("""
                       SELECT COUNT(*)                                              as total_users,
                              COUNT(CASE WHEN password LIKE '$2b$%' THEN 1 END)     as encrypted_users,
                              COUNT(CASE WHEN password NOT LIKE '$2b$%' THEN 1 END) as plain_users
                       FROM sys_user
                       """)

        stats = cursor.fetchone()
        total, encrypted, plain = stats

        print(f"📊 密码加密状态统计:")
        print(f"   总用户数：{total}")
        print(f"   已加密用户：{encrypted}")
        print(f"   明文用户：{plain}")

        if plain > 0:
            print(f"\n⚠️  仍有 {plain} 个用户的密码未加密:")
            cursor.execute("""
                           SELECT username, password
                           FROM sys_user
                           WHERE password NOT LIKE '$2b$%'
                           """)
            plain_users = cursor.fetchall()

            for user in plain_users:
                print(f"   - {user[0]}: {user[1]}")

        cursor.close()
        return plain == 0

    except Exception as e:
        print(f"❌ 验证失败：{str(e)}")
        return False


def execute_sql_step_by_step():
    """逐行执行 SQL 语句并输出结果"""
    print("\n🔍 开始逐行执行 SQL 语句...")

    try:
        # 读取 DDL 文件
        with open('database_ddl.sql', 'r', encoding='utf-8') as f:
            sql_content = f.read()

        # 处理数据库 URL 格式（兼容 SQLAlchemy 格式）
        db_url = settings.DATABASE_URL
        if db_url.startswith('postgresql+psycopg2://'):
            # 转换为 psycopg 可以直接使用的格式
            db_url = db_url.replace('postgresql+psycopg2://', 'postgresql://')
            print(f"🔧 自动转换数据库 URL 格式")

        # 连接数据库
        print("🔌 连接数据库...")
        print(f"🔗 连接字符串：{db_url}")
        # 🔥 修复2：使用新版 psycopg.connect 替代 psycopg2.connect
        conn = psycopg.connect(db_url)
        conn.autocommit = False  # 关闭自动提交，便于回滚
        cursor = conn.cursor()
        print("✅ 数据库连接成功！")

        # 智能分割 SQL 语句（处理 dollar quoting）
        sql_statements = []
        current_statement = []
        in_dollar_quote = False
        dollar_tag = None

        for line in sql_content.split('\n'):
            stripped = line.strip()

            # 检查是否进入 dollar quoting
            if not in_dollar_quote and '$func$' in stripped:
                in_dollar_quote = True
                dollar_tag = '$func$'
                current_statement.append(line)
            # 检查是否退出 dollar quoting
            elif in_dollar_quote and dollar_tag in stripped:
                current_statement.append(line)
                sql_statements.append('\n'.join(current_statement).strip())
                current_statement = []
                in_dollar_quote = False
                dollar_tag = None
            # 在 dollar quoting 内部
            elif in_dollar_quote:
                current_statement.append(line)
            # 普通语句，按分号分割
            elif ';' in line:
                parts = line.split(';')
                for i, part in enumerate(parts):
                    if part.strip():
                        if i < len(parts) - 1:
                            current_statement.append(part + ';')
                            sql_statements.append('\n'.join(current_statement).strip())
                            current_statement = []
                        else:
                            current_statement.append(part)
            else:
                current_statement.append(line)

        # 添加最后一个语句
        if current_statement:
            final_stmt = '\n'.join(current_statement).strip()
            if final_stmt:
                sql_statements.append(final_stmt)

        # 过滤空语句
        sql_statements = [stmt for stmt in sql_statements if stmt.strip()]

        print(f"📝 共计 {len(sql_statements)} 条 SQL 语句需要执行\n")

        success_count = 0
        failed_statements = []

        # 逐条执行 SQL 语句
        for i, statement in enumerate(sql_statements, 1):
            try:
                # 提取语句的第一行作为标识
                first_line = statement.split('\n')[0].strip()
                if first_line.startswith('--'):
                    first_line = statement.split('\n')[1].strip() if len(statement.split('\n')) > 1 else first_line

                print(f"[{i}/{len(sql_statements)}] 执行：{first_line[:50]}{'...' if len(first_line) > 50 else ''}")

                cursor.execute(statement)
                conn.commit()
                print(f"    ✓ 执行成功")
                success_count += 1

            except Exception as e:
                conn.rollback()  # 回滚当前语句
                error_msg = str(e)
                print(f"    ✗ 执行失败：{error_msg}")
                failed_statements.append({
                    'index': i,
                    'statement': first_line[:100],
                    'error': error_msg
                })

                # 对于 DROP 语句失败，通常是可以接受的
                if 'DROP' in statement.upper() and 'does not exist' in error_msg.lower():
                    print(f"    ℹ️  表不存在，跳过 DROP 操作")
                    success_count += 1

                # 对于触发器函数相关的错误，提供特殊处理建议
                elif 'unterminated dollar-quoted string' in error_msg or 'syntax error at or near' in error_msg:
                    if 'update_updated_at_column' in statement:
                        print(f"    ⚠️  触发器函数语法错误，建议单独修复")
                        print(f"    💡 运行：python fix success_count += 1  # 让初始化继续进行

                continue

            # 每执行 10 条语句显示一次进度
            if i % 10 == 0:
                print(
                    f"\n📊 进度：{i}/{len(sql_statements)} 条语句已完成 ({success_count} 成功，{len(failed_statements)} 失败)\n")

        # 关闭连接
        cursor.close()
        conn.close()

        # 输出最终结果
        print("\n" + "=" * 60)
        print("📊 执行结果统计:")
        print(f"   总语句数：{len(sql_statements)}")
        print(f"   成功执行：{success_count}")
        print(f"   执行失败：{len(failed_statements)}")
        print("=" * 60)

        if failed_statements:
            print("\n❌ 失败的语句详情:")
            for failed in failed_statements:
                print(f"   [{failed['index']}] {failed['statement']}...")
                print(f"       错误：{failed['error']}")
            return False
        else:
            print("\n✅ 所有 SQL 语句执行成功！")
            return True

    except FileNotFoundError:
        print("❌ 找不到 database_ddl.sql 文件")
        return False
    except Exception as e:
        print(f"❌ 数据库连接或执行出错：{str(e)}")
        return False


def main():
    """主函数"""
    print("=" * 60)
    print("工时与项目协同管理系统 - 数据库初始化 (详细模式)")
    print("=" * 60)

    try:
        # 检查数据库连接配置
        print(f"🗄️  数据库 URL: {settings.DATABASE_URL}")

        # 处理数据库 URL 格式（兼容 SQLAlchemy 格式）
        db_url = settings.DATABASE_URL
        if db_url.startswith('postgresql+psycopg2://'):
            # 转换为 psycopg 可以直接使用的格式
            db_url = db_url.replace('postgresql+psycopg2://', 'postgresql://')
            print(f"🔧 自动转换数据库 URL 格式")

        # 逐行执行 SQL 语句
        success = execute_sql_step_by_step()

        if success:
            # 加密用户密码
            print("\n" + "=" * 60)
            print("🔐 执行用户密码加密...")
            print("=" * 60)

            # 重新连接以进行密码加密
            # 🔥 修复3：新版连接方式
            conn = psycopg.connect(db_url)
            conn.autocommit = False

            encrypt_success = encrypt_user_passwords(conn)

            if encrypt_success:
                # 验证加密结果
                verify_success = verify_encryption(conn)

                conn.close()

                # 输出初始化信息
                print("\n" + "=" * 60)
                print("🎉 数据库初始化完成！")
                print("=" * 60)
                print("🔐 默认管理员账号:")
                print("   用户名：admin")
                print("   密码：admin123")
                print("\n💡 请根据实际需求修改初始数据和权限配置。")

                if verify_success:
                    print("\n✅ 所有用户密码均已成功加密！")
                else:
                    print("\n⚠️  部分用户密码加密失败，请检查日志")
            else:
                conn.close()
                print("\n❌ 密码加密失败")
                sys.exit(1)
        else:
            print("\n❌ 数据库初始化过程中出现错误，请查看上方详细信息")
            sys.exit(1)

    except Exception as e:
        print(f"\n✗ 脚本执行出错：{str(e)}")
        print("请检查:")
        print("1. 数据库服务是否正常运行")
        print("2. DATABASE_URL 配置是否正确")
        print("3. 是否有足够的数据库权限")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()