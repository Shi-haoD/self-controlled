# Frontend Dockerfile - 支持 docs(项目手册) + playground 完整版
FROM docker.m.daocloud.io/node:22-slim AS frontend

ENV PNPM_HOME="/pnpm"
ENV PATH="$PNPM_HOME:$PATH"
ENV NODE_OPTIONS="--max-old-space-size=4096" \
    TZ=Asia/Shanghai

WORKDIR /app

# 配置国内镜像源
ENV COREPACK_NPM_REGISTRY=https://registry.npmmirror.com

# 👇 【核心修复】给 node:22-slim 安装 GIT（解决docs构建失败！）
RUN apt-get update && \
    apt-get install -y git --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*  # 清理缓存，减小镜像体积

# 安装 pnpm
RUN corepack enable pnpm && \
    pnpm config set registry https://registry.npmmirror.com

# 复制全部项目文件
COPY . /app

# 安装依赖（严格锁定版本）
RUN --mount=type=cache,id=pnpm,target=/pnpm/store pnpm install --frozen-lockfile

# 【你要的功能】同时打包 文档手册(docs) + 演示站点(playground)
RUN pnpm run build --filter=@vben/docs --filter=@vben/playground

# ==================== Nginx 部署阶段 ====================
FROM docker.m.daocloud.io/nginx:stable-alpine AS production

# Nginx 基础配置（支持 mjs 前端文件）
RUN echo "types { application/javascript js mjs; }" > /etc/nginx/conf.d/mjs.conf \
    && rm -rf /etc/nginx/conf.d/default.conf

# 复制 2 份构建产物：playground(前端) + docs(项目手册)
COPY --from=frontend /app/playground/dist /usr/share/nginx/html/
COPY --from=frontend /app/docs/docs/.vitepress/dist /usr/share/nginx/html/docs/

# 复制你本地同级目录的 nginx 配置
COPY ./nginx.conf /etc/nginx/nginx.conf

EXPOSE 8080
CMD ["nginx", "-g", "daemon off;"]