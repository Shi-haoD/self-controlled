# 新增API接口文档

## 1. 退出登录接口

**接口地址**: `POST /api/v1/auth/logout`

**请求头**: 
```
Authorization: your_jwt_token_here
```

**响应示例**:
```json
{
  "code": 0,
  "data": null,
  "message": "退出登录成功"
}
```

## 2. 获取用户所有菜单

**接口地址**: `GET /api/v1/menu/all`

**请求头**: 
```
Authorization: your_jwt_token_here
```

**响应示例**:
```json
{
  "code": 0,
  "data": [
    {
      "path": "/dashboard",
      "component": "/dashboard/index.vue",
      "meta": {
        "title": "仪表板",
        "icon": "dashboard"
      }
    },
    {
      "path": "/worklog",
      "component": "/worklog/index.vue", 
      "meta": {
        "title": "工作日志",
        "icon": "document"
      }
    }
  ],
  "message": "获取菜单成功"
}
```

## 3. 获取系统支持的时区列表

**接口地址**: `GET /api/v1/timezone/getTimezoneOptions`

**请求头**: 
```
Authorization: your_jwt_token_here
```

**响应示例**:
```json
{
  "code": 0,
  "data": [
    {
      "label": "Asia/Shanghai",
      "value": "Asia/Shanghai"
    },
    {
      "label": "America/New York",
      "value": "America/New_York"
    }
  ],
  "message": "获取时区列表成功"
}
```

## 4. 获取用户时区

**接口地址**: `GET /api/v1/timezone/getTimezone`

**请求头**: 
```
Authorization: your_jwt_token_here
```

**响应示例**:
```json
{
  "code": 0,
  "data": "Asia/Shanghai",
  "message": "获取用户时区成功"
}
```

## 5. 设置用户时区

**接口地址**: `POST /api/v1/timezone/setTimezone`

**请求头**: 
```
Authorization: your_jwt_token_here
Content-Type: application/json
```

**请求体**:
```json
{
  "timezone": "America/New_York"
}
```

**响应示例**:
```json
{
  "code": 0,
  "data": null,
  "message": "时区设置成功"
}
```

## 6. 刷新访问令牌

**接口地址**: `POST /api/v1/auth/refresh`

**请求头**: 
```
Authorization: your_jwt_token_here
```

**响应示例**:
```json
{
  "code": 0,
  "data": {
    "accessToken": "new_jwt_token_here"
  },
  "message": "token刷新成功"
}
```

## 错误码说明

- `0`: 成功
- `1001`: 用户名或密码错误
- `4001`: 时区参数不能为空
- `4002`: 无效的时区
- `5001`: 获取菜单失败
- `5002`: 获取时区列表失败
- `5003`: 获取用户时区失败
- `5004`: 设置时区失败
- `5005`: 退出登录失败
- `5006`: token刷新失败