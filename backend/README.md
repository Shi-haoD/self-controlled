# 工时与项目协同管理系统 - 后端服务

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/FastAPI-0.104+-green.svg" alt="FastAPI Version">
  <img src="https://img.shields.io/badge/PostgreSQL-15+-blue.svg" alt="PostgreSQL Version">
  <img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License">
</p>

基于 FastAPI + PostgreSQL 构建的现代化工时与项目协同管理后端服务，提供完整的 RESTful API 接口。

## 🏗️ 项目架构

```
backend/
├── app/
│   ├── main.py                  # 🚀 应用入口点
│   │
│   ├── core/                    # 核心配置模块
│   │   ├── config.py            # 环境配置管理
│   │   ├── database.py          # 数据库连接池
│   │   ├── security.py          # JWT认证 & 密码加密
│   │   └── deps.py              # 依赖注入（认证、权限等）
│   │
│   ├── api/v1/                  # API路由层
│   │   ├── auth.py              # 🔐 认证接口
│   │   ├── user.py              # 👥 用户管理
│   │   ├── worklog.py           # 📝 工时填报
│   │   ├── menu.py              # 📋 菜单管理
│   │   ├── timezone.py          # 🌍 时区处理
│   │   └── project.py           # 📊 项目管理
│   │
│   ├── models/                  # SQLAlchemy ORM模型
│   │   ├── base.py              # 基础模型类
│   │   ├── user.py              # 用户 & 角色模型
│   │   ├── worklog.py           # 工时记录模型
│   │   ├── project.py           # 项目相关模型
│   │   ├── plan.py              # 计划管理模型
│   │   ├── notification.py      # 消息通知模型
│   │   └── report.py            # 报告模板模型
│   │
│   ├── schemas/                 # Pydantic数据校验模型
│   │   ├── user.py              # 用户数据结构
│   │   ├── auth.py              # 认证数据结构
│   │   ├── worklog.py           # 工时数据结构
│   │   └── common.py            # 通用数据结构
│   │
│   ├── crud/                    # 数据库操作层
│   │   ├── base.py              # 基础CRUD操作
│   │   ├── user.py              # 用户相关操作
│   │   ├── worklog.py           # 工时相关操作
│   │   └── project.py           # 项目相关操作
│   │
│   └── utils/                   # 工具函数
│       ├── response.py          # 统一响应格式
│       └── pagination.py        # 分页工具
│
├── database_ddl.sql             # 🗃️ 数据库DDL脚本
├── init_database.py             # 🛠️ 数据库初始化脚本
├── test_database.py             # 🧪 数据库测试脚本
├── DATABASE_README.md           # 📚 数据库使用文档
├── requirements.txt             # 📦 项目依赖
├── .env.example                 # ⚙️ 环境配置示例
└── .env                         # 🔐 本地环境配置
```

## 🌐 API文档

- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc
- **OpenAPI JSON**: http://127.0.0.1:8000/openapi.json

## 🛠️ 环境准备

### 系统要求

- Python 3.8+
- PostgreSQL 15+
- pip 包管理器

### 步骤1：克隆项目并创建虚拟环境

```bash
# 进入项目目录
cd F:\projects\moduleIntegration\self-controlled\backend

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

### 步骤2：配置环境变量

```bash
# 复制环境配置模板
copy .env.example .env

# 编辑 .env 文件，配置数据库连接等信息
notepad .env  # Windows
gedit .env    # Linux
```

.env 配置示例：
```env
DATABASE_URL=postgresql://username:password@localhost:5432/work_management
JWT_SECRET=your-super-secret-key-change-in-production
JWT_EXPIRE_MINUTES=1440
```

## 📦 安装依赖

```bash
# 升级pip到最新版本
python -m pip install --upgrade pip

# 安装项目依赖
pip install -r requirements.txt

# 验证安装
pip list
```

主要依赖包：
- **FastAPI**: 高性能Web框架
- **SQLAlchemy**: ORM数据库工具
- **Pydantic**: 数据校验库
- **Passlib**: 密码加密
- **PyJWT**: JWT令牌处理
- **psycopg[binary,pool]**: PostgreSQL 驱动（3.x 版本）
- **pytz**: 时区处理

## 🗃️ 数据库初始化

### 方法一：使用SQL脚本（推荐）

```bash
# 连接PostgreSQL数据库
psql -h localhost -U your_username -d your_database

# 执行DDL脚本
\i database_ddl.sql
```

### 方法二：使用Python脚本

```bash
# 初始化数据库表结构
python init_database.py

# 测试数据库连接
python test_database.py
```

### 初始数据

默认管理员账号：
- 用户名：`admin`
- 密码：`admin123`
- 角色：超级管理员

> 💡 **安全提醒**：生产环境请务必修改默认密码！

## ▶️ 启动服务

### 开发环境

```bash
# 启动开发服务器（带热重载）
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 生产环境

```bash
# 启动生产服务器（高性能模式）
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Docker部署

```bash
# 构建镜像
docker build -t work-management-backend .

# 运行容器
docker run -p 8000:8000 work-management-backend
```

## 🌐 服务验证

启动成功后，终端显示：
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
```

访问以下地址验证服务：
- **API文档**: http://127.0.0.1:8000/docs
- **健康检查**: http://127.0.0.1:8000/health
- **OpenAPI规范**: http://127.0.0.1:8000/openapi.json

## 📡 核心API接口

### 认证相关
```
POST /api/v1/auth/login        # 用户登录
POST /api/v1/auth/logout       # 用户登出
GET  /api/v1/auth/me           # 获取当前用户信息
```

### 用户管理
```
GET    /api/v1/user/list       # 获取用户列表
POST   /api/v1/user/create     # 创建用户
PUT    /api/v1/user/{id}       # 更新用户
DELETE /api/v1/user/{id}       # 删除用户
```

### 工时填报
```
GET    /api/v1/worklog/list    # 获取工时记录
POST   /api/v1/worklog/create  # 创建工时记录
PUT    /api/v1/worklog/{id}    # 更新工时记录
DELETE /api/v1/worklog/{id}    # 删除工时记录
```

### 项目管理
```
GET    /api/v1/project/list    # 获取项目列表
POST   /api/v1/project/create  # 创建项目
GET    /api/v1/project/{id}    # 获取项目详情
```

## 🧪 测试验证

### 使用curl测试

```bash
# 用户登录
curl -X POST "http://127.0.0.1:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'

# 获取用户信息
curl -X GET "http://127.0.0.1:8000/api/v1/auth/me" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### 使用Python测试

```python
import requests

# 登录获取token
response = requests.post(
    "http://127.0.0.1:8000/api/v1/auth/login",
    json={"username": "admin", "password": "admin123"}
)
token = response.json()["data"]["access_token"]

# 使用token访问受保护接口
headers = {"Authorization": f"Bearer {token}"}
response = requests.get(
    "http://127.0.0.1:8000/api/v1/auth/me",
    headers=headers
)
print(response.json())
```

## 📊 数据库管理

### 连接数据库

```bash
# 使用psql连接
psql -h localhost -U username -d database_name

# 或使用图形化工具
# pgAdmin4, DBeaver, Navicat等
```

### 常用SQL查询

```sql
-- 查看所有用户
SELECT id, username, real_name, role FROM sys_user;

-- 查看今日工时填报
SELECT * FROM work_daily WHERE work_date = CURRENT_DATE;

-- 统计项目工时
SELECT project_name, SUM(actual_hours) as total_hours 
FROM work_daily 
GROUP BY project_name;
```

## 🔧 开发工具推荐

### IDE/编辑器
- **PyCharm Professional** - 功能强大的Python IDE
- **VS Code** - 轻量级编辑器，配合Python插件
- **Vim/Neovim** - 命令行编辑器

### 数据库工具
- **pgAdmin4** - PostgreSQL官方管理工具
- **DBeaver** - 通用数据库管理工具
- **DataGrip** - JetBrains数据库IDE

### API测试工具
- **Postman** - 功能丰富的API测试工具
- **Insomnia** - 现代化API客户端
- **curl/httpie** - 命令行工具

## 🚀 部署指南

### 生产环境部署

1. **配置生产环境**
   ```bash
   # 设置生产环境变量
   export APP_ENV=production
   export DEBUG=false
   export JWT_SECRET=your-production-secret-key
   ```

2. **使用进程管理器**
   ```bash
   # 使用supervisor
   sudo apt-get install supervisor
   # 配置supervisor.conf
   
   # 或使用systemd
   sudo systemctl enable work-management
   ```

3. **反向代理配置**
   ```nginx
   # Nginx配置示例
   server {
       listen 80;
       server_name your-domain.com;
       
       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 📞 技术支持

如有问题，请联系：
- 📧 邮箱：support@example.com
- 🐛 Issues：[GitHub Issues](https://github.com/your-org/work-management/issues)
- 💬 讨论区：[GitHub Discussions](https://github.com/your-org/work-management/discussions)

---

<p align="center">Made with ❤️ by Development Team</p>