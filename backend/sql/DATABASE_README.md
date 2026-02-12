# 工时与项目协同管理系统 - 数据库说明

## 📋 概述

本项目基于PostgreSQL设计了完整的数据库表结构，包含10个核心业务表，支持工时填报、项目管理、权限控制等完整功能。

## 🗃️ 数据库表结构

### 核心表清单

| 表名 | 用途 | 主要字段 |
|------|------|----------|
| `sys_user` | 系统用户表 | 用户基本信息、角色、状态等 |
| `sys_role` | 角色权限表 | 角色定义、权限配置、数据范围 |
| `work_daily` | 每日工作填报表 | 工时记录、项目关联、工作详情 |
| `project_info` | 项目基础信息表 | 项目基本信息、负责人、技术栈 |
| `project_statistic` | 项目统计表 | 项目指标、质量评估、风险等级 |
| `annual_plan` | 年度计划表 | 个人年度计划、进度跟踪 |
| `work_problem` | 工作问题复盘表 | 问题记录、根因分析、整改措施 |
| `sys_message` | 消息通知表 | 系统消息、任务提醒、已读状态 |
| `report_template` | 报告模板表 | 报告模板、格式配置 |
| `work_task` | 任务下发表 | 任务分配、进度跟踪、完成情况 |

## 🚀 使用方式

### 方式一：使用SQL脚本（推荐）

```bash
# 1. 连接到PostgreSQL数据库
psql -h localhost -U your_username -d your_database

# 2. 执行DDL脚本
\i database_ddl.sql
```

### 方式二：使用Python初始化脚本

```bash
# 1. 确保已安装依赖
pip install -r requirements.txt

# 2. 配置环境变量（创建 .env 文件）
echo "DATABASE_URL=postgresql://username:password@localhost:5432/database_name" > .env

# 3. 运行初始化脚本
python init_database.py
```

### 方式三：通过FastAPI应用自动初始化

启动应用时会自动创建表结构：
```bash
uvicorn app.main:app --reload
```

## 🔧 初始数据

脚本会自动创建以下初始数据：

### 默认角色
- 超级管理员 (admin)
- 项目总监 (project_director)  
- 部门经理 (dept_manager)
- 技术经理 (tech_manager)
- 项目经理 (project_manager)
- 普通员工 (employee)

### 默认用户
- 用户名：`admin`
- 密码：`admin123`
- 角色：超级管理员

### 默认报告模板
- 通用日报模板 (Word格式)
- 项目周报模板 (PPT格式)  
- 部门月报模板 (Excel格式)

## 🔐 密码加密说明

默认管理员密码使用bcrypt加密：
```
明文密码: admin123
加密后: $2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/RK.PZvO.S
```

如需修改密码，可使用以下Python代码生成新密码：
```python
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
hashed_password = pwd_context.hash("your_new_password")
print(hashed_password)
```

## 📊 索引优化

已为高频查询字段创建索引：
- 用户相关：用户名、邮箱、部门、角色
- 工作填报：用户ID+日期、项目ID、状态
- 项目相关：负责人、状态、优先级
- 计划相关：用户ID+年份、状态
- 消息通知：接收者、类型、已读状态
- 任务相关：发布者、接收者、截止日期、状态

## ⚙️ 自动更新时间

所有表都配置了自动更新时间戳功能：
- `create_time`: 记录创建时间
- `update_time`: 记录最后更新时间（自动更新）

## 🛡️ 数据完整性约束

- 外键约束确保数据关联性
- 唯一约束防止重复数据
- 非空约束保证必要字段完整性
- 默认值简化数据插入

## 📝 注意事项

1. **生产环境**：请修改默认密码和JWT密钥
2. **权限配置**：根据实际组织结构调整角色权限
3. **数据备份**：定期备份重要业务数据
4. **性能监控**：关注慢查询和索引使用情况
5. **扩展字段**：可根据业务需要添加自定义字段

## 🔄 升级迁移

如需升级数据库结构：
1. 备份现有数据
2. 执行增量DDL脚本
3. 验证数据完整性
4. 更新应用代码

## 📞 技术支持

如有问题请联系开发团队或查看项目文档。

---
*文档版本：V1.0*
*最后更新：2026-02-05*
