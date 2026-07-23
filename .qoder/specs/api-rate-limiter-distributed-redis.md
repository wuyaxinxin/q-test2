# 分布式API速率限制系统 - 实现计划

## 一、项目概述

**目标**: 将现有Java命令行应用(图书管理+台球俱乐部系统)改造为Spring Boot Web应用,实现企业级分布式API速率限制系统

**当前项目状况**:
- 纯Java CLI应用,三层架构(UI → Service → Repository)
- 无Web框架,无构建配置,数据存储在内存HashMap
- 项目路径: `/home/jhdt62081/文档/Qoder2/`

**核心需求**:
- 多种限流算法(令牌桶、滑动窗口)
- 多维度限流(用户ID、IP、端点、用户层级)
- 分布式环境支持(多服务器共享Redis状态)
- 监控与滥用检测(违规记录、黑名单、Prometheus指标)
- 最小性能影响(限流检查延迟 < 10ms)

---

## 二、技术架构

### 2.1 整体架构

```
Client → Load Balancer
         ↓
┌────────────────────────────────────┐
│  Spring Boot Instance 1/2/3...     │
│  ├─ RateLimitFilter (最高优先级)   │
│  ├─ Controller (REST API)          │
│  ├─ Service (复用现有业务逻辑)     │
│  └─ Repository (扩展为JPA)         │
└────────────────────────────────────┘
         ↓                ↓
    Redis Cluster    PostgreSQL
    (限流状态)       (监控数据)
```

**设计原则**:
- **最小侵入**: 保留现有Service/Repository接口,仅修改实现
- **分层职责**: 限流在Filter层处理,与业务逻辑解耦
- **水平扩展**: 无状态服务实例,状态存储在Redis
- **优雅降级**: Redis故障时切换到本地Caffeine缓存限流

### 2.2 技术栈

| 组件 | 选型 | 版本 |
|-----|------|-----|
| Spring Boot | 核心框架 | 2.7.18 |
| Java | 编程语言 | 11+ |
| Redis Client | Redisson | 3.x |
| 构建工具 | Maven | 3.8+ |
| 数据库 | PostgreSQL | 14+ |
| 本地缓存 | Caffeine | 3.x |
| 监控指标 | Micrometer + Prometheus | 1.x |

---

## 三、限流核心设计

### 3.1 令牌桶算法

**Redis数据结构 (Hash)**:
```
Key: rate_limit:token_bucket:{dimension}:{identifier}:{endpoint}
Fields:
  - tokens: 当前令牌数 (double)
  - capacity: 桶容量 (int)
  - refill_rate: 每秒补充速率 (double)
  - last_refill_ts: 上次补充时间戳 (long, 毫秒)
```

**算法流程**:
1. 获取当前时间戳
2. 从Redis读取桶状态
3. 计算应补充的令牌数: `(当前时间 - 上次补充时间) * 补充速率 / 1000`
4. 更新令牌数: `min(当前令牌 + 补充量, 容量)`
5. 判断是否有足够令牌(≥1):
   - 有: 消费1个,返回允许
   - 无: 计算等待时间,返回拒绝

**原子性保证**: 使用Lua脚本一次性完成"读取-计算-写入"操作

**关键文件**:
- `/src/main/java/com/yourcompany/ratelimit/strategy/TokenBucketStrategy.java` (算法实现)
- `/src/main/resources/lua/token_bucket_acquire.lua` (Lua脚本)

### 3.2 滑动窗口算法

**Redis数据结构 (Sorted Set)**:
```
Key: rate_limit:sliding_window:{dimension}:{identifier}:{endpoint}
Score: 请求时间戳(毫秒)
Member: 请求唯一ID(UUID)
```

**算法流程**:
1. 获取当前时间戳
2. 计算窗口起始时间: `当前时间 - 窗口大小`
3. 清理过期数据: `ZREMRANGEBYSCORE key -inf 窗口起始时间`
4. 统计窗口内请求数: `ZCOUNT key 窗口起始时间 当前时间`
5. 判断是否超限:
   - 未超限: 添加当前请求,返回允许
   - 超限: 计算重置时间,返回拒绝

**关键文件**:
- `/src/main/java/com/yourcompany/ratelimit/strategy/SlidingWindowStrategy.java`
- `/src/main/resources/lua/sliding_window_acquire.lua`

### 3.3 限流规则管理

**规则配置来源**:
1. **application.yml** (静态规则,优先级最低)
2. **Redis** (缓存规则,优先级中)
3. **PostgreSQL** (动态规则,优先级最高)

**规则结构**:
```yaml
rate-limit:
  rules:
    - id: books-api-user-tier
      priority: 10
      algorithm: TOKEN_BUCKET
      dimensions: [USER_ID, ENDPOINT]
      scope:
        endpoints: ["/api/books/**"]
        methods: [GET, POST]
        user-tiers: [BASIC, VIP]
      limits:
        BASIC:
          capacity: 10
          refill-rate: 1
        VIP:
          capacity: 50
          refill-rate: 5
```

**规则匹配逻辑**:
- 按优先级排序规则
- 使用Ant路径匹配器匹配endpoint
- 多维度组合(用户+IP+端点)
- 本地Caffeine缓存匹配结果(TTL 5分钟)

**热更新机制**:
- 规则修改后发布Redis Pub/Sub消息
- 所有实例订阅消息,清空本地缓存,重新加载

**关键文件**:
- `/src/main/java/com/yourcompany/ratelimit/service/ratelimit/RateLimitRuleManager.java`

### 3.4 Filter拦截器

**实现层级**: Servlet Filter (优先级最高)

**执行流程**:
1. **白名单检查**: `/actuator/**`、`/metrics`、内网IP快速放行
2. **元数据提取**:
   - IP地址(优先使用X-Forwarded-For)
   - 用户ID(JWT Token解析或Session)
   - 端点路径(规范化处理)
   - 用户层级(从缓存或数据库查询)
3. **限流检查**: 调用RateLimiterService
4. **决策响应**:
   - 允许: 添加响应头(X-RateLimit-Limit/Remaining/Reset),继续处理
   - 拒绝: 返回429状态码 + Retry-After响应头
5. **异步记录**: 监控数据(不阻塞主流程)

**关键文件**:
- `/src/main/java/com/yourcompany/ratelimit/filter/RateLimitingFilter.java`
- `/src/main/java/com/yourcompany/ratelimit/filter/RequestMetadataExtractor.java`

---

## 四、分布式与高可用

### 4.1 Redis集群架构

**部署模式**: Redis Cluster (3主3从)

**配置要点**:
```yaml
spring:
  redis:
    redisson:
      config:
        clusterServersConfig:
          nodeAddresses:
            - "redis://redis-node-1:6379"
            - "redis://redis-node-2:6379"
            - "redis://redis-node-3:6379"
          connectionPoolSize: 64
          readMode: SLAVE  # 读操作走从节点
          retryAttempts: 3
          timeout: 5000
```

**连接池大小计算**:
```
connectionPoolSize = (预期QPS × Redis延迟(ms) / 1000) × 安全系数
示例: (10000 × 5 / 1000) × 1.5 = 75 → 配置64
```

### 4.2 降级方案

**多层降级架构**:
```
REDIS_PRIMARY (默认)
  ↓ [健康检查失败3次]
REDIS_REPLICA (从节点)
  ↓ [集群不可用]
LOCAL_CACHE (Caffeine + Guava RateLimiter)
  ↓ [故障超过5分钟]
PERMISSIVE_MODE (宽松模式,仅记录不拦截)
```

**本地限流策略**:
- 使用Guava RateLimiter实现单机限流
- 限流额度 = 全局限制 / 实例数量 (例: 100 QPS / 3实例 = 33 QPS/实例)
- Caffeine缓存限流器实例(最大10000个,过期时间10分钟)

**健康检查**:
- 定时任务每5秒ping Redis
- 连续3次失败触发降级
- 恢复后持续1分钟稳定才升级回正常

**关键文件**:
- `/src/main/java/com/yourcompany/ratelimit/service/ratelimit/FallbackManager.java`

### 4.3 分布式锁

**使用场景**: 复杂限流逻辑(无法用Lua脚本实现)

**实现方式**: Redisson RLock

**配置**:
```java
RLock lock = redissonClient.getLock(lockKey);
// 等待100ms,持有5s后自动释放
boolean acquired = lock.tryLock(100, 5000, TimeUnit.MILLISECONDS);
```

**锁粒度**: 细粒度锁(单个用户/IP的桶),避免全局锁

**优化策略**: 优先使用Lua脚本,仅在复杂逻辑中使用分布式锁

---

## 五、监控与分析

### 5.1 违规记录存储

**数据库表设计 (PostgreSQL)**:
```sql
CREATE TABLE rate_limit_violations (
  id BIGSERIAL PRIMARY KEY,
  timestamp TIMESTAMP NOT NULL,
  user_id VARCHAR(128),
  ip_address VARCHAR(45) NOT NULL,
  endpoint VARCHAR(512) NOT NULL,
  http_method VARCHAR(10) NOT NULL,
  user_tier VARCHAR(32) NOT NULL,
  rule_id VARCHAR(64) NOT NULL,
  algorithm VARCHAR(32) NOT NULL,
  limit_value INTEGER NOT NULL,
  current_count INTEGER NOT NULL,
  retry_after_seconds INTEGER,
  
  INDEX idx_timestamp (timestamp DESC),
  INDEX idx_user_id (user_id),
  INDEX idx_ip_address (ip_address)
);
```

**批量写入优化**:
- 使用LinkedBlockingQueue缓冲(容量10000)
- 每100条或1秒flush一次
- JPA batch_size配置为100

### 5.2 滥用检测

**检测规则**:
- **短期窗口**: 5分钟内违规20次 → 警告
- **中期窗口**: 1小时内违规100次 → 封禁1小时
- **分布式扫描**: 10秒内访问50+不同端点 → 立即封禁

**黑名单管理**:
- 数据库表存储封禁记录
- Redis缓存黑名单(快速查询)
- 自动解封机制(封禁时间到期)

**关键文件**:
- `/src/main/java/com/yourcompany/ratelimit/monitoring/AbuseDetector.java`
- `/src/main/java/com/yourcompany/ratelimit/repository/jpa/BlacklistRepository.java`

### 5.3 Prometheus指标

**暴露的指标**:
- `rate_limit_requests_total{result, endpoint, tier}` - 请求计数器
- `rate_limit_current_tokens{user_id, endpoint}` - 实时令牌数
- `rate_limit_check_duration_seconds{algorithm}` - 检查延迟
- `rate_limit_blacklist_size{type}` - 黑名单大小

**监控端点**: `/actuator/prometheus`

**Grafana仪表盘面板**:
- 请求通过率趋势图
- Top 10被限流端点
- 用户层级流量分布
- Redis性能监控
- 黑名单趋势

**关键文件**:
- `/src/main/java/com/yourcompany/ratelimit/monitoring/MetricsCollector.java`
- `/src/main/java/com/yourcompany/ratelimit/config/MetricsConfig.java`

---

## 六、实施步骤

### 阶段1: 项目基础改造 (第1-2周)

#### 步骤1: 初始化Spring Boot项目

**创建的文件**:
1. `/pom.xml` - Maven配置,定义所有依赖
2. `/src/main/resources/application.yml` - 主配置文件
3. `/src/main/resources/application-dev.yml` - 开发环境配置
4. `/src/main/resources/application-prod.yml` - 生产环境配置
5. `/src/main/resources/logback-spring.xml` - 日志配置
6. `/src/main/java/com/yourcompany/ratelimit/RateLimiterApplication.java` - Spring Boot启动类

**关键依赖**:
- spring-boot-starter-web (REST API)
- spring-boot-starter-data-jpa (数据持久化)
- spring-boot-starter-data-redis (Redis操作)
- redisson-spring-boot-starter (分布式功能)
- spring-boot-starter-actuator (健康检查)
- micrometer-registry-prometheus (监控)
- caffeine (本地缓存)

#### 步骤2: 包结构重组

**目标结构**:
```
src/main/java/com/yourcompany/ratelimit/
├── RateLimiterApplication.java
├── config/                     # 配置类
│   ├── RedisConfig.java
│   ├── AsyncConfig.java
│   └── MetricsConfig.java
├── filter/                     # 过滤器层
│   ├── RateLimitingFilter.java (核心)
│   └── RequestMetadataExtractor.java
├── service/                    # 业务层
│   ├── ratelimit/             # 限流服务
│   │   ├── RateLimiterService.java
│   │   ├── RateLimitRuleManager.java (核心)
│   │   └── FallbackManager.java (核心)
│   ├── library/               # 图书业务(迁移)
│   └── billiard/              # 台球业务(迁移)
├── controller/                 # REST API层
│   ├── LibraryController.java
│   └── BilliardController.java
├── repository/                 # 数据访问层
│   ├── redis/
│   │   └── RedisRateLimitRepository.java
│   └── jpa/
│       ├── ViolationRecordRepository.java
│       └── BlacklistRepository.java
├── strategy/                   # 限流算法
│   ├── TokenBucketStrategy.java (核心)
│   ├── SlidingWindowStrategy.java (核心)
│   └── RateLimiterStrategyFactory.java
├── model/                      # 数据模型
│   ├── entity/
│   ├── dto/
│   └── enums/
└── monitoring/                 # 监控组件
    ├── RateLimitMonitoringService.java
    ├── AbuseDetector.java
    └── MetricsCollector.java
```

**迁移策略**:
- 保留现有`library/service`和`billiard/service`的接口,仅修改实现类(HashMap → JPA)
- 现有`library/model`和`billiard/model`迁移到新包结构,添加JPA注解
- `ConsoleUI`逻辑转换为REST Controller

#### 步骤3: 数据持久化改造

**数据库Schema创建**:
- `/src/main/resources/db/migration/V1__init_schema.sql` (Flyway迁移脚本)
- 业务表: books, readers, borrow_records, members, booking_records
- 限流表: rate_limit_violations, abuse_blacklist, api_usage_statistics

**Repository层迁移**:
- 创建JPA Repository接口: `BookJpaRepository extends JpaRepository<Book, String>`
- 更新Service实现类注入新Repository
- 保留Service接口不变(业务逻辑层API稳定)

#### 步骤4: 创建REST API层

**Controller设计**:
- `LibraryController`: 图书管理API
  - `GET /api/books` - 查询图书列表
  - `POST /api/books` - 添加图书
  - `GET /api/books/{id}` - 查询图书详情
  - `PUT /api/books/{id}` - 更新图书
  - `DELETE /api/books/{id}` - 删除图书
- `BorrowController`: 借阅管理API
  - `POST /api/borrow` - 借书
  - `PUT /api/return/{id}` - 还书
- `RateLimitAdminController`: 限流规则管理API
  - `GET /api/admin/rate-limit/rules` - 查询规则
  - `POST /api/admin/rate-limit/rules` - 创建规则
  - `PUT /api/admin/rate-limit/rules/{id}` - 更新规则

**统一返回格式**:
```json
{
  "success": true,
  "data": {...},
  "error": null,
  "timestamp": "2026-01-07T10:30:00Z"
}
```

### 阶段2: 限流核心实现 (第3-4周)

#### 步骤5: Redis集成与Lua脚本

**Redis配置类**:
- `/src/main/java/com/yourcompany/ratelimit/config/RedisConfig.java`
- 配置Redisson客户端
- 配置连接池、序列化器、健康检查

**Lua脚本管理**:
- `/src/main/resources/lua/token_bucket_acquire.lua` - 令牌桶原子操作
- `/src/main/resources/lua/sliding_window_acquire.lua` - 滑动窗口原子操作
- `/src/main/java/com/yourcompany/ratelimit/repository/redis/RedisLuaScriptRepository.java` - 脚本加载执行类

**脚本加载方式**:
```java
DefaultRedisScript<List> script = new DefaultRedisScript<>();
script.setScriptText(luaScriptContent);
script.setResultType(List.class);

List<Long> result = redisTemplate.execute(
  script,
  Collections.singletonList(bucketKey),
  capacity, refillRate, System.currentTimeMillis()
);
```

#### 步骤6: 限流算法实现

**令牌桶算法**:
- `/src/main/java/com/yourcompany/ratelimit/strategy/TokenBucketStrategy.java`
- 实现`RateLimitStrategy`接口
- 核心方法: `RateLimitResult tryAcquire(RequestMetadata metadata, RateLimitRule rule)`
- 调用Lua脚本执行原子操作
- 返回结果包含: 是否允许、剩余配额、重试时间

**滑动窗口算法**:
- `/src/main/java/com/yourcompany/ratelimit/strategy/SlidingWindowStrategy.java`
- 使用Redis Sorted Set存储请求时间戳
- 清理过期数据 + 统计 + 添加记录一次完成(Lua脚本)

**策略工厂**:
- `/src/main/java/com/yourcompany/ratelimit/strategy/RateLimiterStrategyFactory.java`
- 根据规则的algorithm字段(TOKEN_BUCKET或SLIDING_WINDOW)选择策略
- 使用Spring依赖注入管理策略实例

#### 步骤7: 规则管理器实现

**规则加载**:
- `/src/main/java/com/yourcompany/ratelimit/service/ratelimit/RateLimitRuleManager.java`
- 启动时从application.yml + Redis + PostgreSQL加载所有规则
- 使用Caffeine本地缓存(容量10000,TTL 5分钟)

**规则匹配**:
- 使用`AntPathMatcher`匹配endpoint路径
- 按优先级排序规则(priority字段,数字越小越优先)
- 多维度组合(用户ID + IP + 端点)

**热更新机制**:
- 监听Redis Pub/Sub频道: `rate_limit_rule_update`
- 收到消息后清空本地缓存,重新加载规则
- 热更新延迟 < 500ms

#### 步骤8: Filter集成

**Filter实现**:
- `/src/main/java/com/yourcompany/ratelimit/filter/RateLimitingFilter.java`
- 继承`OncePerRequestFilter`
- 优先级设置为最高: `@Order(Ordered.HIGHEST_PRECEDENCE)`

**核心逻辑**:
1. 白名单检查(健康检查端点、静态资源、内网IP)
2. 元数据提取(IP、用户ID、端点、用户层级)
3. 调用`RateLimiterService.tryAcquire(metadata)`
4. 允许: 添加响应头 + 继续处理 + 异步记录
5. 拒绝: 返回429错误 + Retry-After响应头 + 异步记录违规

**注册Filter**:
- `/src/main/java/com/yourcompany/ratelimit/config/FilterConfig.java`
- 使用`FilterRegistrationBean`注册
- 设置URL匹配模式: `/api/*`

### 阶段3: 监控与降级 (第5周)

#### 步骤9: 监控服务实现

**异步监控服务**:
- `/src/main/java/com/yourcompany/ratelimit/monitoring/RateLimitMonitoringService.java`
- 使用`@Async`注解实现异步记录
- 批量插入违规记录(每100条或1秒flush)
- 更新Redis统计计数器

**滥用检测器**:
- `/src/main/java/com/yourcompany/ratelimit/monitoring/AbuseDetector.java`
- 多窗口统计违规次数(5分钟、1小时、1天)
- 检测分布式扫描(短时间访问大量不同端点)
- 自动加入黑名单(写入数据库 + Redis缓存)

**Prometheus指标收集**:
- `/src/main/java/com/yourcompany/ratelimit/monitoring/MetricsCollector.java`
- 自定义Counter、Gauge、Timer
- 暴露`/actuator/prometheus`端点

#### 步骤10: 降级系统实现

**降级管理器**:
- `/src/main/java/com/yourcompany/ratelimit/service/ratelimit/FallbackManager.java`
- 定时任务每5秒ping Redis健康检查
- 降级状态机: REDIS_PRIMARY → REDIS_REPLICA → LOCAL_CACHE → PERMISSIVE_MODE

**本地限流器**:
- 使用Guava `RateLimiter`作为降级方案
- Caffeine缓存限流器实例(最大10000个,过期时间10分钟)
- 限流额度 = 全局限制 / 实例数量

**告警集成**:
- `/src/main/java/com/yourcompany/ratelimit/monitoring/AlertService.java`
- 降级时发送告警(钉钉/邮件/Slack)
- 告警级别: INFO → WARN → ERROR → CRITICAL

### 阶段4: 测试与优化 (第6周)

#### 步骤11: 单元测试

**测试覆盖**:
- `TokenBucketStrategyTest`: 令牌消费、耗尽、补充、并发安全
- `SlidingWindowStrategyTest`: 窗口计数、过期清理、边界条件
- `RateLimitRuleManagerTest`: 规则加载、匹配、热更新
- `FallbackManagerTest`: 健康检查、降级、恢复

**测试工具**:
- JUnit 5 + Mockito
- Testcontainers (Embedded Redis)
- AssertJ (流式断言)

#### 步骤12: 集成测试

**端到端测试场景**:
- 单实例限流准确性: 配置10 QPS,发送15个请求,验证前10个通过
- 分布式环境一致性: 3实例共享30 QPS,每个发送15个,总通过≈30
- Redis故障降级: 停止Redis,验证切换到本地限流
- 滥用检测与封禁: 快速违规50次,验证自动黑名单
- 热更新规则: 通过API更新规则,验证1秒内生效

**压力测试**:
- 工具: JMeter/Gatling
- 目标: 10000 QPS,延迟P99 < 50ms
- 验证: 限流准确性 > 95%

#### 步骤13: 性能优化

**优化点**:
1. Redis连接池调优(connectionPoolSize: 64)
2. Lua脚本优化(减少Redis命令数)
3. Caffeine缓存预热(启动时加载热点数据)
4. 异步日志(Logback AsyncAppender)
5. JVM参数调优(G1GC、-Xmx4g)

### 阶段5: 部署与运维 (第7周)

#### 步骤14: Docker容器化

**Dockerfile**:
- `/Dockerfile` - 多阶段构建
- 基础镜像: openjdk:11-jre-slim
- 包含健康检查脚本

**Docker Compose**:
- `/docker-compose.yml` - 本地开发环境
- 包含: App × 3 + Redis Cluster + PostgreSQL + Prometheus + Grafana

#### 步骤15: Kubernetes部署

**K8s资源文件**:
- `/k8s/deployment.yaml` - Deployment(3副本)
- `/k8s/service.yaml` - ClusterIP Service
- `/k8s/ingress.yaml` - Nginx Ingress
- `/k8s/configmap.yaml` - 配置文件
- `/k8s/secret.yaml` - Redis密码等敏感信息

#### 步骤16: 监控与告警

**Grafana仪表盘**:
- 导入预定义Dashboard JSON
- 配置Prometheus数据源
- 设置告警规则(拒绝率>30%、Redis Down等)

**日志聚合**:
- ELK Stack集成(Logstash收集)
- 日志格式: JSON结构化
- 敏感信息脱敏

---

## 七、关键文件清单

以下是实施过程中最关键的文件路径及其作用:

### 核心限流组件

1. **`/src/main/java/com/yourcompany/ratelimit/filter/RateLimitingFilter.java`**
   - **作用**: 限流系统入口点,拦截所有HTTP请求并执行限流检查
   - **重要性**: 整个系统的核心控制器,决定请求是否放行

2. **`/src/main/java/com/yourcompany/ratelimit/strategy/TokenBucketStrategy.java`**
   - **作用**: 令牌桶算法核心实现,处理突发流量
   - **重要性**: 包含关键的Lua脚本调用逻辑,决定限流准确性

3. **`/src/main/resources/lua/token_bucket_acquire.lua`**
   - **作用**: 保证令牌桶操作原子性的Lua脚本
   - **重要性**: 直接决定限流准确性和性能

4. **`/src/main/java/com/yourcompany/ratelimit/service/ratelimit/RateLimitRuleManager.java`**
   - **作用**: 规则管理器,负责加载、缓存、匹配、热更新规则
   - **重要性**: 系统灵活性的关键,支持动态配置

5. **`/src/main/java/com/yourcompany/ratelimit/service/ratelimit/FallbackManager.java`**
   - **作用**: 降级管理器,处理Redis故障场景
   - **重要性**: 保证系统高可用性,生产环境容错核心

### 配置文件

6. **`/pom.xml`**
   - **作用**: Maven项目配置,定义所有依赖
   - **重要性**: 项目基础,决定技术栈

7. **`/src/main/resources/application.yml`**
   - **作用**: 主配置文件(Redis、数据库、限流规则)
   - **重要性**: 核心配置,决定系统行为

8. **`/src/main/resources/lua/sliding_window_acquire.lua`**
   - **作用**: 滑动窗口算法的Lua脚本
   - **重要性**: 滑动窗口限流的原子操作实现

### 监控与降级

9. **`/src/main/java/com/yourcompany/ratelimit/monitoring/AbuseDetector.java`**
   - **作用**: 滥用检测器,识别异常流量模式
   - **重要性**: 安全防护核心,自动封禁恶意请求

10. **`/src/main/java/com/yourcompany/ratelimit/monitoring/MetricsCollector.java`**
    - **作用**: Prometheus指标收集器
    - **重要性**: 系统可观测性基础

---

## 八、潜在风险与应对

### 8.1 时钟漂移问题

**风险**: 分布式环境中服务器时钟不同步,导致令牌桶补充不准确

**应对**:
- 部署NTP时间同步(所有服务器每小时同步)
- 监控时钟偏移,超过1秒告警
- 容忍误差: ±100ms对限流影响极小

### 8.2 Redis连接失败

**风险**: Redis主节点故障或网络分区导致限流不可用

**应对**:
- Redis Sentinel自动故障转移(<30秒)
- 降级到本地Caffeine缓存限流
- 连接超时设置(5秒),快速失败
- 断路器模式(Resilience4j)

### 8.3 高并发竞态条件

**风险**: 多个请求同时读写令牌桶,导致令牌超发

**应对**:
- Lua脚本保证原子性(首选方案)
- Redisson分布式锁(复杂逻辑备选)
- 锁粒度细化(单个用户/IP的桶)

### 8.4 缓存穿透攻击

**风险**: 恶意请求不存在的userId,绕过缓存直接打到Redis/DB

**应对**:
- 布隆过滤器快速判断userId是否存在
- 空值缓存(缓存"不存在"的结果)
- 请求签名验证(HMAC)
- IP黑名单 + 速率限制(检测到穿透自动封禁)

---

## 九、性能指标

### 9.1 延迟目标

| 指标 | 目标值 |
|-----|-------|
| 限流检查延迟P50 | < 5ms |
| 限流检查延迟P95 | < 10ms |
| 限流检查延迟P99 | < 50ms |
| Redis命令延迟 | < 5ms |

### 9.2 吞吐量目标

- 单实例: > 10000 QPS
- 3实例集群: > 30000 QPS
- 错误率: < 0.1%

### 9.3 资源消耗

- JVM堆内存: 2-4GB
- Redis连接数: 64/实例
- PostgreSQL连接数: 20/实例

---

## 十、总结

本计划将现有Java CLI应用改造为企业级分布式API速率限制系统,核心要点:

1. **架构改造**: CLI → Spring Boot Web应用,三层架构保留
2. **限流算法**: 令牌桶(突发流量) + 滑动窗口(平滑限流)
3. **分布式支持**: Redis Cluster共享状态,Lua脚本保证原子性
4. **高可用**: 多层降级(Redis → 本地缓存 → 宽松模式)
5. **监控分析**: Prometheus指标 + 滥用检测 + 黑名单
6. **性能优化**: 连接池调优 + 本地缓存 + 异步处理

**最关键的5个文件**:
1. `RateLimitingFilter.java` (入口点)
2. `TokenBucketStrategy.java` (核心算法)
3. `token_bucket_acquire.lua` (原子性保证)
4. `RateLimitRuleManager.java` (规则管理)
5. `FallbackManager.java` (降级容错)

**实施周期**: 6-7周
- 第1-2周: 项目基础改造
- 第3-4周: 限流核心实现
- 第5周: 监控与降级
- 第6周: 测试与优化
- 第7周: 部署与运维
