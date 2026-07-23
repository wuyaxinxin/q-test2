# Student类扩展实现规范

## 一、任务概述

为 `student.java` 文件添加新的成员变量和toString方法,增强Student类的数据结构和输出能力。

## 二、修改文件

**主要修改文件:** `/Users/admin/Documents/testQoder/Qoder2/student.java`

## 三、当前状态分析

student.java 现有结构:
- 文件头部注释: `// 自由万岁` 和 `// 始终生效`
- 成员变量: name(String)、age(int)
- 构造器: Student(String name, int age)
- Getter方法: getName()、getAge()
- 缺少: setter方法、toString方法

## 四、实现方案

### 1. 添加成员变量

在现有的 age 变量之后添加三个新的私有成员变量:

```java
private String studentId;  // 学生ID
private String email;      // 电子邮箱
private String major;      // 专业
```

**字段顺序:**
- name (现有)
- age (现有)
- studentId (新增)
- email (新增)
- major (新增)

### 2. 构造器设计

**方案: 保留原有构造器 + 添加完整构造器**

- **保留:** `Student(String name, int age)` - 向后兼容
- **新增:** `Student(String name, int age, String studentId, String email, String major)` - 初始化所有字段

**参数顺序:** 按照成员变量声明顺序 - name, age, studentId, email, major

### 3. Getter方法

为新增的三个字段添加标准Getter方法:
- `public String getStudentId()`
- `public String getEmail()`
- `public String getMajor()`

**方法顺序:** 按照字段声明顺序,放在现有getter之后

### 4. Setter方法

为所有字段添加Setter方法:
- 现有字段: `setName(String name)`, `setAge(int age)`
- 新增字段: `setStudentId(String studentId)`, `setEmail(String email)`, `setMajor(String major)`

**方法顺序:** 按照字段声明顺序,放在所有getter之后

### 5. toString方法实现

**格式要求:** `Student: [name: xx, age: xx, studentId: xx, email: xx, major: xx]`

**实现要点:**
- 添加 `@Override` 注解
- 使用详细格式输出所有字段
- 格式: "字段名: 字段值",字段间用", "分隔
- 以"Student: ["开头,以"]"结尾
- 字段顺序与成员变量声明顺序一致

**示例输出:**
```
Student: [name: 张三, age: 20, studentId: 2024001, email: zhangsan@example.com, major: 计算机科学]
```

## 五、代码结构顺序

修改后的完整类结构顺序:
1. 文件头部注释(保持不变)
2. 类声明
3. 成员变量(5个)
4. 构造器(2个: 原有 + 新增)
5. Getter方法(5个: getName, getAge, getStudentId, getEmail, getMajor)
6. Setter方法(5个: setName, setAge, setStudentId, setEmail, setMajor)
7. toString方法
8. 类结束

## 六、代码规范遵循

根据项目规则:
- ✅ 文件头部保留 `// 自由万岁` 和 `// 始终生效`
- ✅ 所有成员变量使用 private 修饰符
- ✅ Getter/Setter遵循JavaBean命名规范
- ✅ 缩进保持一致(4空格)
- ✅ 方法之间保持空行分隔

## 七、实现步骤

1. **Step 1:** 在第6行(age变量声明)之后插入三个新成员变量
2. **Step 2:** 在现有构造器之后添加5参数构造器
3. **Step 3:** 在getAge()方法之后添加三个新的getter方法
4. **Step 4:** 在所有getter方法之后添加5个setter方法
5. **Step 5:** 在所有setter方法之后添加toString方法
6. **Step 6:** 验证代码格式和缩进一致性

## 八、技术要点

- **封装性:** 所有字段private,通过getter/setter访问
- **兼容性:** 保留原有构造器,确保现有代码不受影响
- **规范性:** 严格遵循JavaBean规范
- **可读性:** toString方法提供清晰的对象状态输出

## 九、关键文件

- `/Users/admin/Documents/testQoder/Qoder2/student.java` - 主要修改目标
