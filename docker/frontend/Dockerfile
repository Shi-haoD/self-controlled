# Frontend Dockerfile - 优化内存占用
FROM docker.m.daocloud.io/node:22-slim AS frontend

ENV PNPM_HOME="/pnpm"
ENV PATH="$PNPM_HOME:$PATH"
ENV NODE_OPTIONS="--max-old-space-size=4096" \
    TZ=Asia/Shanghai

WORKDIR /app

# 配置使用国内镜像源并安装 pnpm
ENV COREPACK_NPM_REGISTRY=https://registry.npmmirror.com
RUN corepack enable pnpm && \
    pnpm config set registry https://registry.npmmirror.com

# 仅复制必要的文件
#COPY package.json pnpm-lock.yaml pnpm-workspace.yaml turbo.json ./
#COPY internal/ ./internal/
#COPY packages/ ./packages/
#COPY scripts/turbo-run/ ./scripts/turbo-run/
#COPY scripts/vsh/ ./scripts/vsh/
#COPY apps/web-antd/ ./apps/web-antd/
#COPY playground/.env.production playground/index.html playground/package.json playground/vite.config.mts playground/tsconfig.json playground/tsconfig.node.json ./playground/
#COPY playground/src/ ./playground/src/
#COPY playground/public/ ./playground/public/
#COPY scripts/deploy/nginx.conf ./scripts/deploy/nginx.conf
WORKDIR /app

# copy package.json and pnpm-lock.yaml to workspace
COPY . /app

# 安装依赖（使用国内镜像源）
RUN --mount=type=cache,id=pnpm,target=/pnpm/store pnpm install --frozen-lockfile

# 构建前端
RUN pnpm run build --filter=\!./docs

FROM docker.m.daocloud.io/nginx:stable-alpine AS production

# 配置 nginx
#RUN rm -rf /etc/nginx/conf.d/default.conf

# 配置 nginx
RUN echo "types { application/javascript js mjs; }" > /etc/nginx/conf.d/mjs.conf \
    && rm -rf /etc/nginx/conf.d/default.conf

# 复制构建产物
COPY --from=frontend /app/playground/dist /usr/share/nginx/html

# 复制 nginx 配置
#COPY --from=frontend /app/scripts/deploy/nginx.conf /etc/nginx/nginx.conf
COPY --from=frontend nginx.conf /etc/nginx/nginx.conf
EXPOSE 8080

CMD ["nginx", "-g", "daemon off;"]
