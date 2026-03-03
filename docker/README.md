# Self Controlled Docker 部署说明

## 📋 项目信息

- **前端端口**: 8080 (与 dify 的 8083 端口不冲突)
- **后端端口**: 8000
- **数据库端口**: 5432
- **总内存限制**: ~2.5GB (优化后，确保与 dify 共存不卡死)

## 📦 服务说明

### 容器列表
- `self_postgres`: PostgreSQL 16 数据库 (512MB 限制)
- `self_backend`: FastAPI 后端服务 (1GB 限制)
- `self_frontend`: Nginx 前端服务 (512MB 限制)

### 资源分配
- **PostgreSQL**: 512MB
- **Backend**: 1GB (2 workers)
- **Frontend**: 512MB
- **总计**: ~2.5GB (剩余 3.5GB 给 dify 和其他进程)

## 🔧 配置说明

### 环境变量
在 `docker-compose.yml` 中修改以下配置：

```yaml
environment:
  DATABASE_URL: postgresql://admin:password123@postgres:5432/work_management
  JWT_SECRET: your-super-secret-key-change-in-production
  APP_ENV: production
  DEBUG: "false"
```

### 数据持久化
数据库数据存储在 Docker volume `postgres_data` 中。

## 🛠️ 常用命令

### 启动所有服务
```powershell
docker-compose up -d --build
```

### 查看服务状态
```powershell
docker-compose ps
```

### 查看日志
```powershell
docker-compose logs -f
```

### 重启某个服务
```powershell
docker-compose restart backend
```

### 停止所有服务
```powershell
docker-compose down
```

### 进入容器
```powershell
docker exec -it self_backend sh
docker exec -it self_postgres psql -U admin -d work_management
```

## ⚙️ Docker Desktop 设置建议

打开 Docker Desktop Settings → Resources：
- **CPU**: 建议分配 4 核以上
- **Memory**: 6GB（与 dify 共存足够）
- **Swap**: 1GB
- **Disk Image Size**: 至少 20GB 可用空间

## 🔍 故障排查

### 内存不足
如果提示内存不足，编辑 `docker-compose.yml`，将后端 worker 数量改为 1：
```yaml
command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 1
```

### 端口冲突
检查端口占用：
```powershell
netstat -ano | findstr :8080
netstat -ano | findstr :8000
```

### 数据库初始化失败
```powershell
docker exec -it self_backend python /app/sql/init_database.py
```

## 📊 健康检查

### 测试 API
```powershell
curl http://localhost:8000/health
```

### 测试前端
浏览器访问：http://localhost:8080

## 🎯 与 dify 共存优化

本配置已针对与 dify 共存进行了优化：
1. **端口隔离**: dify(8083) vs 本项目 (8080)
2. **内存限制**: 每个容器都有明确的内存上限
3. **资源复用**: 共享 Docker 网络，减少开销
4. **最小化镜像**: 仅包含必要文件

## 📝 注意事项

1. **首次启动较慢**: 需要下载镜像和初始化数据库，请耐心等待
2. **备份数据**: 重要数据请定期备份
3. **密码安全**: 生产环境请修改默认密码
