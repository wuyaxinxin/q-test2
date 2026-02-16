"""辅助工具函数"""
from typing import Dict, Any
from datetime import datetime


def format_datetime(dt: datetime, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """格式化日期时间
    
    Args:
        dt: 日期时间对象
        format_str: 格式字符串
        
    Returns:
        str: 格式化后的字符串
    """
    if not dt:
        return ""
    return dt.strftime(format_str)


def calculate_gpa(score: float) -> float:
    """计算GPA绩点
    
    Args:
        score: 成绩分数
        
    Returns:
        float: 绩点
    """
    if score >= 90:
        return 4.0
    elif score >= 85:
        return 3.7
    elif score >= 82:
        return 3.3
    elif score >= 78:
        return 3.0
    elif score >= 75:
        return 2.7
    elif score >= 72:
        return 2.3
    elif score >= 68:
        return 2.0
    elif score >= 64:
        return 1.7
    elif score >= 60:
        return 1.0
    else:
        return 0.0


def get_grade_level(score: float) -> str:
    """获取成绩等级
    
    Args:
        score: 成绩分数
        
    Returns:
        str: 等级
    """
    if score >= 90:
        return "A"
    elif score >= 85:
        return "A-"
    elif score >= 82:
        return "B+"
    elif score >= 78:
        return "B"
    elif score >= 75:
        return "B-"
    elif score >= 72:
        return "C+"
    elif score >= 68:
        return "C"
    elif score >= 64:
        return "C-"
    elif score >= 60:
        return "D"
    else:
        return "F"


def calculate_score_distribution(scores: list[float]) -> Dict[str, int]:
    """计算分数段分布
    
    Args:
        scores: 成绩列表
        
    Returns:
        Dict[str, int]: 各分数段人数
    """
    distribution = {
        "excellent": 0,  # 90-100
        "good": 0,       # 80-89
        "medium": 0,     # 70-79
        "passing": 0,    # 60-69
        "failing": 0     # <60
    }
    
    for score in scores:
        if score >= 90:
            distribution["excellent"] += 1
        elif score >= 80:
            distribution["good"] += 1
        elif score >= 70:
            distribution["medium"] += 1
        elif score >= 60:
            distribution["passing"] += 1
        else:
            distribution["failing"] += 1
    
    return distribution


def success_response(data: Any = None, message: str = "操作成功") -> Dict:
    """构建成功响应
    
    Args:
        data: 响应数据
        message: 响应消息
        
    Returns:
        Dict: 响应字典
    """
    return {
        "code": 200,
        "message": message,
        "data": data
    }


def error_response(message: str, code: int = 400, errors: list = None) -> Dict:
    """构建错误响应
    
    Args:
        message: 错误消息
        code: 错误码
        errors: 错误详情列表
        
    Returns:
        Dict: 响应字典
    """
    response = {
        "code": code,
        "message": message
    }
    if errors:
        response["errors"] = errors
    return response
