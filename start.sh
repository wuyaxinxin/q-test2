#!/bin/bash
# 学生管理系统启动脚本

echo "========================================"
echo "学生管理系统启动脚本"
echo "========================================"

# 检查Python版本
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到 Python3,请先安装 Python 3.8+"
    exit 1
fi

echo "步骤 1/3: 安装依赖包..."
python3 -m pip install -q -r requirements.txt

echo "步骤 2/3: 初始化数据库..."
python3 init_db.py

echo "步骤 3/3: 启动应用..."
echo ""
echo "应用启动中..."
echo "访问地址: http://localhost:8000"
echo "API文档: http://localhost:8000/docs"
echo ""
echo "初始账号:"
echo "  管理员: admin / admin123"
echo "  教师: teacher001 / teacher123"
echo ""
echo "按 Ctrl+C 停止服务器"
echo "========================================"

python3 main.py
