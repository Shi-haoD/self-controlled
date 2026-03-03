# Frontend Dockerfile - 优化内存占用
FROM docker.m.daocloud.io/node:22-alpine AS frontend

ENV PNPM_HOME="/pnpm"
ENV PATH="$PNPM_HOME:$PATH"
ENV NODE_OPTIONS="--max-old-space-size=4096" \
    TZ=Asia/Shanghai

WORKDIR /app

# 安装 pnpm
RUN corepack enable && corepack prepare pnpm@latest --activate

# 仅复制必要的文件
COPY package.json pnpm-lock.yaml pnpm-workspace.yaml turbo.json ./
COPY internal/ ./internal/
COPY packages/ ./packages/
COPY apps/web-antd/ ./apps/web-antd/
COPY playground/ ./playground/
COPY scripts/deploy/nginx.conf ./scripts/deploy/nginx.conf

# 安装依赖
RUN --mount=type=cache,id=pnpm,target=/pnpm/store pnpm install --frozen-lockfile

# 构建前端
RUN pnpm run build:play

FROM docker.m.daocloud.io/nginx:alpine AS production

# 配置 nginx
RUN echo "types { application/javascript js mjs; }" > /etc/nginx/conf.d/mjs.conf \
    && rm -rf /etc/nginx/conf.d/default.conf

# 复制构建产物
COPY --from=frontend /app/playground/dist /usr/share/nginx/html

# 复制 nginx 配置
COPY --from=frontend /app/scripts/deploy/nginx.conf /etc/nginx/nginx.conf

EXPOSE 8080

CMD ["nginx", "-g", "daemon off;"]
