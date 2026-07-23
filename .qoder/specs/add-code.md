# 始终生效

# config.py 配置管理类实现规范

## 概述

为 `/Users/admin/.qoder/worktree/Qoder2/bKFjsZ/config.py` 添加配置管理类和便捷函数。

## 当前状态

```python
name="张三"
age="24"
age="23"
```

## 实现目标

1. 在文件顶部添加 `# 始终生效` 注释
2. 整理变量，移除重复的 `age="24"` 赋值
3. 添加 `ConfigManager` 配置管理类
4. 添加模块级便捷函数

## 实现步骤

### 步骤 1: 添加文件头注释
- 在文件第一行添加 `# 始终生效`

### 步骤 2: 整理模块级变量
- 保留 `name="张三"`
- 只保留 `age="23"`（移除重复的 `age="24"`）

### 步骤 3: 实现 ConfigManager 类

```python
class ConfigManager:
    def __init__(self, defaults=None):
        """初始化配置管理器"""
        self._defaults = defaults.copy() if defaults else {}
        self._config = self._defaults.copy()
    
    def get(self, key, default=None):
        """获取配置值"""
        return self._config.get(key, default)
    
    def set(self, key, value):
        """设置配置值"""
        self._config[key] = value
    
    def get_all(self):
        """获取所有配置"""
        return self._config.copy()
    
    def has(self, key):
        """检查配置是否存在"""
        return key in self._config
    
    def update(self, config_dict):
        """批量更新配置"""
        self._config.update(config_dict)
    
    def reset(self):
        """重置为默认值"""
        self._config = self._defaults.copy()
```

### 步骤 4: 创建全局实例和便捷函数

```python
config = ConfigManager({"name": name, "age": age})

def get_config(key, default=None):
    return config.get(key, default)

def get_all_config():
    return config.get_all()
```

## 关键文件

- **修改**: `/Users/admin/.qoder/worktree/Qoder2/bKFjsZ/config.py`

## 使用方式

```python
# 传统方式（保持兼容）
import config
print(config.name)  # "张三"

# 通过配置管理器
from config import config
print(config.get("name"))

# 通过便捷函数
from config import get_config
print(get_config("age"))
```
