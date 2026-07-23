# Food.java 深拷贝与浅拷贝实现规范

## 任务概述
为 Food.java 添加深拷贝和浅拷贝方法,使 Food 对象能够被安全地复制。

## 关键文件
- **主要修改文件**: `/home/jhdt62081/文档/Qoder2/Food.java`
- **参考文件**: `/home/jhdt62081/文档/Qoder2/Point.java` (拷贝构造函数模式)

## 当前 Food 类结构

```java
public class Food {
    private Point position;  // 食物位置
    private Random random;   // 随机数生成器
    
    public Food() {
        random = new Random();
        position = new Point(0, 0);
    }
    
    // 已有方法: generate(), getPosition(), setPosition()
}
```

## 实现方案

### 1. 深拷贝构造函数
**插入位置**: 第 22 行后(现有构造函数之后)

```java
/**
 * 深拷贝构造函数
 * 创建完全独立的 Food 对象副本,包括新的 Point 和 Random 实例
 * @param other 要拷贝的 Food 对象
 */
public Food(Food other) {
    if (other.position != null) {
        this.position = new Point(other.position);
    } else {
        this.position = null;
    }
    this.random = new Random();
}
```

**设计要点**:
- 使用 Point 的拷贝构造函数创建新的 Point 对象(确保位置独立)
- 创建新的 Random 实例(确保随机序列独立)
- 添加 null 检查以提高安全性

### 2. 深拷贝方法
**插入位置**: 深拷贝构造函数之后

```java
/**
 * 创建当前 Food 对象的深拷贝
 * 深拷贝会创建完全独立的对象,所有引用类型字段都会被复制
 * 修改副本不会影响原对象
 * 
 * @return 独立的 Food 对象副本
 */
public Food deepCopy() {
    return new Food(this);
}
```

**设计要点**:
- 委托给拷贝构造函数实现,避免代码重复
- 确保完全独立性

### 3. 浅拷贝方法
**插入位置**: 深拷贝方法之后

```java
/**
 * 创建当前 Food 对象的浅拷贝
 * 浅拷贝会创建新的 Food 对象,但 position 和 random 引用与原对象共享
 * 修改共享字段会同时影响原对象和副本
 * 
 * @return 部分共享的 Food 对象副本
 */
public Food shallowCopy() {
    Food copy = new Food();
    copy.position = this.position;
    copy.random = this.random;
    return copy;
}
```

**设计要点**:
- 直接复制引用,不创建新对象
- position 和 random 在原对象和副本之间共享

## 代码组织

**方法顺序**:
1. 无参构造函数 (已存在)
2. 深拷贝构造函数 (新增)
3. 深拷贝方法 `deepCopy()` (新增)
4. 浅拷贝方法 `shallowCopy()` (新增)
5. 现有的业务方法 (generate, getPosition, setPosition)

## 设计决策说明

### 深拷贝 vs 浅拷贝
- **深拷贝**: 创建完全独立的对象,所有引用类型字段都创建新实例
- **浅拷贝**: 创建新 Food 对象,但引用字段指向相同对象

### Random 字段处理
- **深拷贝**: 创建新 Random 实例,确保随机序列独立
- **浅拷贝**: 共享 Random 引用,两个对象产生关联的随机序列

### Point 字段处理
- **深拷贝**: 使用 Point 的拷贝构造函数 `new Point(other.position)`
- **浅拷贝**: 直接复制引用 `copy.position = this.position`

## 遵循项目规则

- 文件开头的"始终生效"和"模型决策"注释保持不变
- 遵循现有的 JavaDoc 注释风格
- 与 Point 类的拷贝构造函数模式保持一致

## 实现检查清单

- [ ] 深拷贝构造函数已添加且包含 null 检查
- [ ] deepCopy() 方法已添加并委托给拷贝构造函数
- [ ] shallowCopy() 方法已添加并直接复制引用
- [ ] 所有方法都有完整的 JavaDoc 注释
- [ ] 代码风格与现有代码一致
- [ ] 文件头部规则注释未被修改
