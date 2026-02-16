# 学生管理系统

基于 FastAPI 的学生管理系统,提供学生信息管理、成绩管理、课程管理、统计分析等功能。

## 功能特性

- **用户认证**: JWT令牌认证,支持多角色(管理员、教师、学生)
- **学生管理**: 学生信息的增删改查,支持分页和筛选
- **成绩管理**: 成绩录入、批量录入、查询和统计
- **课程管理**: 课程信息管理
- **班级管理**: 班级信息管理
- **统计分析**: 学生成绩统计、班级成绩统计、课程成绩统计
- **数据验证**: 完善的数据验证机制
- **API文档**: 自动生成的 Swagger/ReDoc 文档

## 技术栈

- **框架**: FastAPI 0.104+
- **数据库**: SQLite (可切换至 PostgreSQL)
- **ORM**: SQLAlchemy 2.0+
- **认证**: JWT (python-jose)
- **数据验证**: Pydantic 2.0+
- **测试**: Pytest
- **Web服务器**: Uvicorn

## 项目结构

```
student-management-system/
├── app/
│   ├── api/                    # API路由层
│   │   ├── v1/                 # API v1版本
│   │   │   ├── auth.py         # 认证接口
│   │   │   ├── students.py     # 学生接口
│   │   │   ├── grades.py       # 成绩接口
│   │   │   └── statistics.py   # 统计接口
│   │   └── deps.py             # 依赖注入
│   ├── core/                   # 核心配置
│   │   ├── config.py           # 应用配置
│   │   ├── security.py         # 安全模块
│   │   ├── database.py         # 数据库配置
│   │   └── middleware.py       # 中间件
│   ├── models/                 # 数据模型
│   ├── schemas/                # Pydantic模式
│   ├── services/               # 业务逻辑层
│   ├── repositories/           # 数据访问层
│   └── utils/                  # 工具函数
├── tests/                      # 测试目录
├── main.py                     # 应用入口
├── init_db.py                  # 数据库初始化
└── requirements.txt            # 依赖包
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 初始化数据库

```bash
python init_db.py
```

初始账号信息:
- 管理员: `admin` / `admin123`
- 教师: `teacher001` / `teacher123`

### 3. 启动应用

```bash
python main.py
```

或使用 uvicorn:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 4. 访问API文档

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API接口说明

### 认证接口

- `POST /api/v1/auth/login` - 用户登录
- `POST /api/v1/auth/refresh` - 刷新令牌
- `PUT /api/v1/auth/password` - 修改密码
- `GET /api/v1/auth/me` - 获取当前用户信息

### 学生管理接口

- `POST /api/v1/students` - 创建学生 (需要管理员权限)
- `GET /api/v1/students` - 查询学生列表 (支持分页和筛选)
- `GET /api/v1/students/{student_id}` - 查询学生详情
- `PUT /api/v1/students/{student_id}` - 更新学生信息
- `DELETE /api/v1/students/{student_id}` - 删除学生

### 成绩管理接口

- `POST /api/v1/grades` - 录入成绩
- `POST /api/v1/grades/batch` - 批量录入成绩
- `GET /api/v1/grades/student/{student_id}` - 查询学生成绩
- `PUT /api/v1/grades/{grade_id}` - 更新成绩
- `DELETE /api/v1/grades/{grade_id}` - 删除成绩

### 统计分析接口

- `GET /api/v1/statistics/student/{student_id}` - 学生成绩统计
- `GET /api/v1/statistics/class/{class_id}` - 班级成绩统计
- `GET /api/v1/statistics/course/{course_id}` - 课程成绩统计

## 运行测试

```bash
# 运行所有测试
pytest

# 运行单元测试
pytest tests/unit/

# 运行集成测试
pytest tests/integration/

# 查看测试覆盖率
pytest --cov=app tests/
```

## 配置说明

配置文件位于 `app/core/config.py`,主要配置项:

- `DATABASE_URL`: 数据库连接URL
- `SECRET_KEY`: JWT密钥 (生产环境务必修改)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: 访问令牌过期时间
- `CORS_ORIGINS`: 允许的跨域源

也可以通过 `.env` 文件配置(参考 `.env.example`)。

## 权限说明

### 角色定义

- **超级管理员(admin)**: 拥有所有权限
- **教师(teacher)**: 可查看学生信息、录入成绩、查看统计
- **学生(student)**: 只能查看自己的信息和成绩

### 权限矩阵

| 功能 | 管理员 | 教师 | 学生 |
|-----|-------|------|------|
| 学生管理 | ✓ | 查看 | 查看本人 |
| 成绩录入 | ✓ | ✓ | ✗ |
| 成绩查看 | ✓ | ✓ | 本人 |
| 统计报表 | ✓ | ✓ | 本人 |

## 开发指南

### 添加新功能

1. 在 `models/` 中定义数据模型
2. 在 `schemas/` 中定义Pydantic模式
3. 在 `repositories/` 中实现数据访问
4. 在 `services/` 中实现业务逻辑
5. 在 `api/v1/` 中实现API接口
6. 编写单元测试和集成测试

### 代码规范

- 遵循 PEP 8 编码规范
- 使用类型注解
- 添加完整的文档字符串
- 编写测试用例

## 注意事项

1. **生产环境部署**:
   - 修改 `SECRET_KEY` 为强密码
   - 使用 PostgreSQL 等生产级数据库
   - 配置 HTTPS
   - 设置合理的 CORS 策略

2. **安全性**:
   - 定期更新依赖包
   - 使用强密码策略
   - 限制API访问频率
   - 记录审计日志

## 许可证

MIT License

## 联系方式

如有问题或建议,请提交 Issue。
