# 系统管理API接口文档

## 权限码管理接口

### 获取用户权限码
```
GET /api/v1/system/codes
```
**说明**: 获取当前登录用户的权限码列表
**响应示例**:
```json
{
  "code": 0,
  "data": ["AC_100100", "AC_100010"],
  "message": "获取权限码成功"
}
```

### 获取所有权限码
```
GET /api/v1/system/codes/all
```
**说明**: 获取系统所有权限码（管理员接口）
**响应示例**:
```json
{
  "code": 0,
  "data": [
    {
      "code": "AC_100100",
      "name": "超级权限1",
      "description": "超级管理员专属权限1",
      "resourceType": "menu"
    }
  ],
  "message": "获取权限码列表成功"
}
```

## 菜单管理接口

### 获取用户菜单
```
GET /api/v1/system/menus
```
**说明**: 获取当前用户有权访问的菜单树
**响应示例**:
```json
{
  "code": 0,
  "data": [
    {
      "id": 1,
      "name": "Dashboard",
      "path": "/dashboard",
      "component": "/dashboard/analytics/index",
      "meta": {
        "title": "page.dashboard.title"
      },
      "children": [...]
    }
  ],
  "message": "获取菜单成功"
}
```

### 获取所有菜单
```
GET /api/v1/system/menus/all
```
**说明**: 获取系统所有菜单（管理员接口）
**响应示例**:
```json
{
  "code": 0,
  "data": [
    {
      "id": 1,
      "pid": null,
      "name": "Dashboard",
      "path": "/dashboard",
      "component": "/dashboard/analytics/index",
      "type": "catalog",
      "status": 1,
      "authCode": null,
      "sortOrder": 0,
      "children": [...]
    }
  ],
  "message": "获取菜单列表成功"
}
```

### 获取扁平化菜单列表
```
GET /api/v1/system/menus/list
```
**说明**: 获取扁平化的菜单列表（用于表格展示）
**响应示例**:
```json
{
  "code": 0,
  "data": [
    {
      "id": 1,
      "pid": null,
      "name": "Dashboard",
      "path": "/dashboard",
      "component": "/dashboard/analytics/index",
      "type": "catalog",
      "status": 1,
      "authCode": null,
      "sortOrder": 0
    }
  ],
  "message": "获取菜单列表成功"
}
```

## 时区管理接口

### 获取时区列表
```
GET /api/v1/system/timezones
```
**说明**: 获取系统支持的时区列表
**响应示例**:
```json
{
  "code": 0,
  "data": [
    {
      "id": 1,
      "timezone": "Asia/Shanghai",
      "offset": 8,
      "displayName": "中国标准时间 (UTC+8)",
      "countryCode": "CN"
    }
  ],
  "message": "获取时区列表成功"
}
```

### 获取时区选项
```
GET /api/v1/system/timezones/options
```
**说明**: 获取时区选项（用于前端选择器）
**响应示例**:
```json
{
  "code": 0,
  "data": [
    {
      "value": "Asia/Shanghai",
      "label": "中国标准时间 (UTC+8)"
    }
  ],
  "message": "获取时区选项成功"
}
```

## 使用说明

1. **认证**: 所有接口都需要JWT Token认证，请求头添加 `Authorization: Bearer <token>`
2. **权限**: 部分接口需要特定权限才能访问
3. **数据格式**: 所有响应都遵循统一的 `{code, data, message}` 格式
4. **错误处理**: 错误时code为非0值，message包含错误描述

## 前端集成示例

```javascript
// 获取用户菜单
const getMenuData = async () => {
  try {
    const response = await fetch('/api/v1/system/menus', {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    });
    const result = await response.json();
    if (result.code === 0) {
      return result.data;
    }
  } catch (error) {
    console.error('获取菜单失败:', error);
  }
};

// 获取权限码
const getUserPermissions = async () => {
  try {
    const response = await fetch('/api/v1/system/codes', {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    });
    const result = await response.json();
    return result.code === 0 ? result.data : [];
  } catch (error) {
    console.error('获取权限失败:', error);
    return [];
  }
};
```