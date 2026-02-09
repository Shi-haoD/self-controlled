# 工时与项目协同管理系统

一个基于现代技术栈的团队工时管理与项目协同平台，支持智能分析和自动化报告生成。

## 🚀 项目特色

- **智能填报**：AI辅助工时填报，自动分析工作内容
- **多维管理**：项目信息、年度计划、问题复盘一体化管理
- **权限控制**：完善的RBAC权限体系，支持多角色协同
- **数据可视化**：丰富的图表展示，直观了解项目进展
- **智能报告**：自动生成多格式(PPT/PDF/Word/Excel)工作报告
- **容器部署**：Docker一键部署，快速上线使用

## 🛠 技术栈

### 后端
- **FastAPI** + Pydantic + SQLAlchemy 2.0
- **PostgreSQL** 15+ 数据库
- **Redis** 7+ 缓存与消息队列
- **JWT** 认证与权限控制
- **Celery** 异步任务处理

### 前端
- **Vue 3** + Vite + Pinia
- **Element Plus** 组件库
- **ECharts** 数据可视化
- **TailwindCSS** 样式框架

### AI集成
- 大模型API (OpenAI/文心一言)
- LangChain 流程编排

## 📁 项目结构

```
self-controlled/
├── backend/           # 后端服务
│   ├── app/           # 核心应用代码
│   │   ├── api/       # API接口
│   │   ├── core/      # 核心配置
│   │   ├── models/    # 数据模型
│   │   └── schemas/   # 数据验证
│   └── requirements.txt
├── frontend/          # 前端应用
│   ├── apps/          # 多套UI主题
│   │   ├── web-antd/   # Ant Design版本
│   │   ├── web-ele/    # Element Plus版本
│   │   └── web-naive/  # Naive UI版本
│   └── package.json
└── README.md
```

## 🔧 快速开始

### 环境要求
- Python 3.8+
- Node.js 16+
- Docker (可选)
- PostgreSQL 15+

### 后端启动

```bash
cd backend
# 安装依赖
pip install -r requirements.txt

# 初始化数据库
python init_database.py

# 启动服务
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 前端启动

```bash
cd frontend
# 安装依赖
pnpm install

# 启动开发服务器
pnpm dev
```

### Docker部署

```bash
# 构建并启动所有服务
docker-compose up -d --build

# 查看服务状态
docker-compose ps
```

## 🎯 核心功能

### 1. 工时管理
- 📅 每日工时填报
- 🤖 AI智能分析
- 📊 工时统计报表
- ⏰ 自动提醒功能

### 2. 项目管理
- 📋 项目信息维护
- 👥 团队成员管理
- 📈 项目进度跟踪
- 🐛 BUG统计分析

### 3. 计划管理
- 📆 年度计划制定
- 🎯 月度目标分解
- 🔄 进度实时更新
- ⚠️ 风险预警提醒

### 4. 问题复盘
- 📝 问题记录分类
- 🔍 根因深度分析
- 💡 整改措施跟踪
- 📊 效果量化评估

### 5. 智能报告
- 📊 数据自动汇总
- 🤖 AI内容生成
- 📄 多格式导出
- 🎨 模板化定制

## 🔐 权限体系

| 角色 | 权限范围 | 核心功能 |
|------|----------|----------|
| 普通员工 | 个人数据 | 工时填报、个人统计 |
| 项目经理 | 项目数据 | 项目管理、团队统计 |
| 部门经理 | 部门数据 | 部门报表、绩效分析 |
| 系统管理员 | 全部数据 | 系统配置、用户管理 |

## 📱 界面预览

系统提供多套UI主题：
- Element Plus风格 (推荐)
- Ant Design风格  
- Naive UI风格
- TDesign风格

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解更多详情。

## 📞 联系我们

- 项目主页: [GitHub仓库地址]
- 问题反馈: [Issues页面]
- 邮箱联系: [your-email@example.com]

---
*Made with ❤️ using FastAPI + Vue3*