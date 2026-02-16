# API接口清单

## 基础信息

- **基础URL**: `http://localhost:8000`
- **API版本**: v1
- **API前缀**: `/api/v1`
- **认证方式**: Bearer Token (JWT)

## 通用响应格式

### 成功响应
```json
{
  "code": 200,
  "message": "操作成功",
  "data": { ... }
}
```

### 错误响应
```json
{
  "code": 400,
  "message": "错误描述",
  "errors": [ ... ]
}
```

### 状态码说明
- `200` - 请求成功
- `201` - 创建成功
- `400` - 请求参数错误
- `401` - 未授权,需要登录
- `403` - 权限不足
- `404` - 资源不存在
- `409` - 数据冲突
- `500` - 服务器内部错误

---

## 1. 认证接口

### 1.1 用户登录

**接口**: `POST /api/v1/auth/login`

**权限**: 无需认证

**请求体**:
```json
{
  "username": "admin",
  "password": "admin123"
}
```

**响应**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800,
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### 1.2 刷新令牌

**接口**: `POST /api/v1/auth/refresh`

**权限**: 无需认证

**请求参数**:
- `refresh_token` (string, required): 刷新令牌

**响应**:
```json
{
  "access_token": "new_token",
  "token_type": "bearer",
  "expires_in": 1800
}
```

### 1.3 修改密码

**接口**: `PUT /api/v1/auth/password`

**权限**: 已登录用户

**请求头**:
```
Authorization: Bearer YOUR_TOKEN
```

**请求体**:
```json
{
  "old_password": "admin123",
  "new_password": "newpassword123"
}
```

**响应**:
```json
{
  "code": 200,
  "message": "密码修改成功"
}
```

### 1.4 获取当前用户信息

**接口**: `GET /api/v1/auth/me`

**权限**: 已登录用户

**请求头**:
```
Authorization: Bearer YOUR_TOKEN
```

**响应**:
```json
{
  "id": 1,
  "username": "admin",
  "email": "admin@example.com",
  "full_name": "系统管理员",
  "role": "admin",
  "is_active": true,
  "created_at": "2024-10-23T10:00:00",
  "updated_at": null
}
```

---

## 2. 学生管理接口

### 2.1 创建学生

**接口**: `POST /api/v1/students`

**权限**: 管理员

**请求头**:
```
Authorization: Bearer YOUR_TOKEN
Content-Type: application/json
```

**请求体**:
```json
{
  "student_id": "2024006",
  "name": "张三",
  "age": 20,
  "gender": "male",
  "major": "计算机科学与技术",
  "class_id": 1,
  "phone": "13800138000",
  "email": "zhangsan@example.com",
  "id_card": "110101199001011234",
  "enrollment_date": "2024-09-01",
  "address": "北京市海淀区"
}
```

**字段说明**:
- `student_id` (string, required): 学号,7位数字
- `name` (string, required): 姓名,2-100字符
- `age` (integer, required): 年龄,0-150
- `gender` (string, required): 性别,male/female
- `major` (string, required): 专业
- `class_id` (integer, optional): 班级ID
- `phone` (string, optional): 手机号
- `email` (string, optional): 邮箱
- `id_card` (string, optional): 身份证号,18位
- `enrollment_date` (date, required): 入学日期
- `address` (string, optional): 地址

**响应**:
```json
{
  "id": 6,
  "student_id": "2024006",
  "name": "张三",
  "age": 20,
  "gender": "male",
  "major": "计算机科学与技术",
  "class_id": 1,
  "class_name": "计算机2024-1班",
  "phone": "13800138000",
  "email": "zhangsan@example.com",
  "id_card": "110101199001011234",
  "enrollment_date": "2024-09-01",
  "status": "active",
  "address": "北京市海淀区",
  "created_at": "2024-10-23T10:00:00",
  "updated_at": null
}
```

### 2.2 查询学生列表

**接口**: `GET /api/v1/students`

**权限**: 教师或管理员

**请求头**:
```
Authorization: Bearer YOUR_TOKEN
```

**查询参数**:
- `page` (integer, default=1): 页码
- `size` (integer, default=20): 每页大小,1-100
- `name` (string, optional): 姓名筛选(模糊匹配)
- `class_id` (integer, optional): 班级ID筛选
- `major` (string, optional): 专业筛选
- `status` (string, optional): 状态筛选(active/graduated/suspended)

**示例**:
```
GET /api/v1/students?page=1&size=20&major=计算机科学
```

**响应**:
```json
{
  "total": 100,
  "page": 1,
  "size": 20,
  "items": [
    {
      "id": 1,
      "student_id": "2024001",
      "name": "张三",
      "age": 20,
      "gender": "male",
      "major": "计算机科学与技术",
      "class_id": 1,
      "class_name": "计算机2024-1班",
      "status": "active",
      ...
    }
  ]
}
```

### 2.3 查询学生详情

**接口**: `GET /api/v1/students/{student_id}`

**权限**: 
- 管理员和教师可查看任意学生
- 学生只能查看本人

**请求头**:
```
Authorization: Bearer YOUR_TOKEN
```

**路径参数**:
- `student_id` (string): 学号

**示例**:
```
GET /api/v1/students/2024001
```

**响应**:
```json
{
  "id": 1,
  "student_id": "2024001",
  "name": "张三",
  "age": 20,
  "gender": "male",
  "major": "计算机科学与技术",
  "class_id": 1,
  "class_name": "计算机2024-1班",
  "phone": "13800138000",
  "email": "zhangsan@example.com",
  "enrollment_date": "2024-09-01",
  "status": "active",
  "created_at": "2024-09-23T10:00:00"
}
```

### 2.4 更新学生信息

**接口**: `PUT /api/v1/students/{student_id}`

**权限**: 管理员

**请求头**:
```
Authorization: Bearer YOUR_TOKEN
Content-Type: application/json
```

**路径参数**:
- `student_id` (string): 学号

**请求体**(所有字段可选):
```json
{
  "name": "李四",
  "age": 21,
  "phone": "13900139000",
  "email": "lisi@example.com",
  "address": "上海市浦东新区",
  "class_id": 2,
  "status": "active"
}
```

**响应**: 返回更新后的学生信息

### 2.5 删除学生

**接口**: `DELETE /api/v1/students/{student_id}`

**权限**: 管理员

**请求头**:
```
Authorization: Bearer YOUR_TOKEN
```

**路径参数**:
- `student_id` (string): 学号

**响应**:
```json
{
  "code": 200,
  "message": "删除成功"
}
```

---

## 3. 成绩管理接口

### 3.1 录入成绩

**接口**: `POST /api/v1/grades`

**权限**: 教师或管理员

**请求头**:
```
Authorization: Bearer YOUR_TOKEN
Content-Type: application/json
```

**请求体**:
```json
{
  "student_id": 1,
  "course_id": 1,
  "score": 85.5,
  "semester": "2024春",
  "academic_year": 2024,
  "exam_date": "2024-06-20",
  "grade_type": "期末"
}
```

**字段说明**:
- `student_id` (integer, required): 学生ID
- `course_id` (integer, required): 课程ID
- `score` (float, required): 成绩,0-100
- `semester` (string, required): 学期
- `academic_year` (integer, required): 学年,2000-2100
- `exam_date` (date, optional): 考试日期
- `grade_type` (string, required): 成绩类型(期中/期末/平时)

**响应**:
```json
{
  "id": 1,
  "student_id": 1,
  "student_name": "张三",
  "course_id": 1,
  "course_name": "数据结构",
  "score": 85.5,
  "semester": "2024春",
  "academic_year": 2024,
  "exam_date": "2024-06-20",
  "grade_type": "期末",
  "recorded_at": "2024-10-23T10:00:00",
  "recorded_by": 2,
  "recorder_name": "张老师"
}
```

### 3.2 批量录入成绩

**接口**: `POST /api/v1/grades/batch`

**权限**: 教师或管理员

**请求头**:
```
Authorization: Bearer YOUR_TOKEN
Content-Type: application/json
```

**请求体**:
```json
{
  "course_id": 1,
  "semester": "2024春",
  "academic_year": 2024,
  "grade_type": "期末",
  "exam_date": "2024-06-20",
  "grades": [
    {"student_id": 1, "score": 85.5},
    {"student_id": 2, "score": 92.0},
    {"student_id": 3, "score": 78.5}
  ]
}
```

**响应**:
```json
{
  "success_count": 2,
  "failed_items": [
    {
      "student_id": 3,
      "error": "学生ID 3 不存在"
    }
  ]
}
```

### 3.3 查询学生成绩

**接口**: `GET /api/v1/grades/student/{student_id}`

**权限**: 
- 管理员和教师可查看任意学生成绩
- 学生只能查看本人成绩

**请求头**:
```
Authorization: Bearer YOUR_TOKEN
```

**路径参数**:
- `student_id` (integer): 学生ID

**查询参数**:
- `semester` (string, optional): 学期筛选
- `academic_year` (integer, optional): 学年筛选
- `course_id` (integer, optional): 课程筛选

**示例**:
```
GET /api/v1/grades/student/1?semester=2024春
```

**响应**:
```json
{
  "items": [
    {
      "id": 1,
      "student_id": 1,
      "student_name": "张三",
      "course_id": 1,
      "course_name": "数据结构",
      "score": 85.5,
      "semester": "2024春",
      "academic_year": 2024,
      "grade_type": "期末",
      "recorded_at": "2024-10-23T10:00:00"
    }
  ],
  "average_score": 85.5,
  "total_credits": 4
}
```

### 3.4 更新成绩

**接口**: `PUT /api/v1/grades/{grade_id}`

**权限**: 教师或管理员

**请求头**:
```
Authorization: Bearer YOUR_TOKEN
Content-Type: application/json
```

**路径参数**:
- `grade_id` (integer): 成绩ID

**请求体**:
```json
{
  "score": 90.0
}
```

**响应**: 返回更新后的成绩信息

### 3.5 删除成绩

**接口**: `DELETE /api/v1/grades/{grade_id}`

**权限**: 管理员

**请求头**:
```
Authorization: Bearer YOUR_TOKEN
```

**路径参数**:
- `grade_id` (integer): 成绩ID

**响应**:
```json
{
  "code": 200,
  "message": "删除成功"
}
```

---

## 4. 统计分析接口

### 4.1 学生成绩统计

**接口**: `GET /api/v1/statistics/student/{student_id}`

**权限**: 
- 管理员和教师可查看任意学生统计
- 学生只能查看本人统计

**请求头**:
```
Authorization: Bearer YOUR_TOKEN
```

**路径参数**:
- `student_id` (integer): 学生ID

**查询参数**:
- `semester` (string, optional): 学期筛选
- `academic_year` (integer, optional): 学年筛选

**示例**:
```
GET /api/v1/statistics/student/1?semester=2024春
```

**响应**:
```json
{
  "average_score": 85.5,
  "highest_score": 95.0,
  "lowest_score": 78.0,
  "passing_rate": 100.0,
  "total_credits": 12,
  "gpa": 3.5
}
```

### 4.2 班级成绩统计

**接口**: `GET /api/v1/statistics/class/{class_id}`

**权限**: 教师或管理员

**请求头**:
```
Authorization: Bearer YOUR_TOKEN
```

**路径参数**:
- `class_id` (integer): 班级ID

**查询参数**:
- `semester` (string, optional): 学期筛选
- `course_id` (integer, optional): 课程筛选

**示例**:
```
GET /api/v1/statistics/class/1?semester=2024春&course_id=1
```

**响应**:
```json
{
  "average_score": 82.5,
  "highest_score": 95.0,
  "lowest_score": 65.0,
  "passing_rate": 95.0,
  "score_distribution": {
    "excellent": 5,
    "good": 10,
    "medium": 8,
    "passing": 5,
    "failing": 2
  }
}
```

### 4.3 课程成绩统计

**接口**: `GET /api/v1/statistics/course/{course_id}`

**权限**: 教师或管理员

**请求头**:
```
Authorization: Bearer YOUR_TOKEN
```

**路径参数**:
- `course_id` (integer): 课程ID

**查询参数**:
- `semester` (string, optional): 学期筛选
- `academic_year` (integer, optional): 学年筛选

**示例**:
```
GET /api/v1/statistics/course/1?semester=2024春
```

**响应**:
```json
{
  "average_score": 82.5,
  "passing_rate": 95.0,
  "excellent_rate": 20.0,
  "score_distribution": {
    "excellent": 10,
    "good": 15,
    "medium": 10,
    "passing": 8,
    "failing": 2
  }
}
```

---

## 5. 其他接口

### 5.1 根路径

**接口**: `GET /`

**权限**: 无

**响应**:
```json
{
  "message": "欢迎使用学生管理系统",
  "version": "1.0.0",
  "docs": "/docs"
}
```

### 5.2 健康检查

**接口**: `GET /health`

**权限**: 无

**响应**:
```json
{
  "status": "healthy"
}
```

### 5.3 API文档

- **Swagger UI**: `GET /docs`
- **ReDoc**: `GET /redoc`

---

## 错误码说明

| 错误码 | 说明 | 示例 |
|-------|------|------|
| 400 | 请求参数错误 | 数据验证失败 |
| 401 | 未授权 | Token无效或过期 |
| 403 | 权限不足 | 学生尝试访问管理员接口 |
| 404 | 资源不存在 | 学号不存在 |
| 409 | 数据冲突 | 学号重复 |
| 422 | 业务错误 | 班级已满 |
| 500 | 服务器错误 | 内部异常 |

---

## Postman测试集

可以使用以下步骤测试API:

1. **获取Token**:
   - POST `/api/v1/auth/login`
   - Body: `{"username":"admin","password":"admin123"}`
   - 复制返回的 `access_token`

2. **设置认证**:
   - 在后续请求的Header中添加:
   - `Authorization: Bearer YOUR_TOKEN`

3. **测试学生管理**:
   - 创建学生: POST `/api/v1/students`
   - 查询列表: GET `/api/v1/students`
   - 查询详情: GET `/api/v1/students/2024001`

4. **测试成绩管理**:
   - 录入成绩: POST `/api/v1/grades`
   - 查询成绩: GET `/api/v1/grades/student/1`

5. **测试统计**:
   - 学生统计: GET `/api/v1/statistics/student/1`

---

**文档版本**: v1.0.0  
**更新时间**: 2025-10-23  
**在线文档**: http://localhost:8000/docs
