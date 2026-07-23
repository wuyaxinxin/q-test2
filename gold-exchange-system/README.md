# 黄金汇率转换系统 (Gold Exchange System)

这是一个基于Spring Boot的Web应用程序，用于计算美元(USD)与黄金之间的汇率转换。

## 功能特性

- 实时美元与黄金汇率转换
- 支持美元到黄金盎司的转换
- 支持黄金盎司到美元的转换
- 清晰的用户界面
- REST API接口

## 技术栈

- Java 11+
- Spring Boot 2.7.0
- Thymeleaf (模板引擎)
- Bootstrap 5 (前端框架)
- Maven (构建工具)

## 安装和运行

1. 确保系统已安装Java 11+ 和 Maven 3.6+

2. 克隆或下载项目代码

3. 进入项目目录：
   ```bash
   cd gold-exchange-system
   ```

4. 使用Maven运行应用程序：
   ```bash
   mvn spring-boot:run
   ```

5. 应用程序将在 `http://localhost:8080` 上运行

## API 接口

- `GET /api/rate` - 获取当前黄金价格(美元/盎司)

## 项目结构

```
gold-exchange-system/
├── pom.xml
├── src/main/java/com/currency/
│   ├── GoldExchangeApplication.java
│   ├── controller/
│   │   └── CurrencyController.java
│   ├── service/
│   │   └── CurrencyService.java
│   └── model/
│       └── CurrencyConversion.java
├── src/main/resources/
│   ├── application.properties
│   ├── templates/
│   │   ├── index.html
│   │   └── result.html
│   └── static/
│       ├── css/
│       │   └── style.css
│       └── js/
│           └── app.js
└── src/test/java/
    └── com/currency/
        ├── GoldExchangeApplicationTests.java
        └── service/
            └── CurrencyServiceTest.java
```

## 使用说明

1. 访问主页 `http://localhost:8080`
2. 输入要转换的金额
3. 选择原始货币类型(美元或黄金盎司)
4. 选择目标货币类型
5. 点击"转换"按钮查看结果

## 测试

运行单元测试：
```bash
mvn test
```

## 打包部署

打包为可执行JAR文件：
```bash
mvn clean package
```

运行打包后的应用程序：
```bash
java -jar target/gold-exchange-system-0.0.1-SNAPSHOT.jar
```