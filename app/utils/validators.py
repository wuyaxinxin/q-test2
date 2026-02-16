"""数据验证工具"""
import re
from typing import Optional
from app.utils.exceptions import ValidationException


def validate_student_id(student_id: str) -> bool:
    """验证学号格式
    
    格式: 4位年份+3位序号,如 2024001
    
    Args:
        student_id: 学号
        
    Returns:
        bool: 是否有效
        
    Raises:
        ValidationException: 格式错误时抛出
    """
    pattern = r'^\d{7}$'
    if not re.match(pattern, student_id):
        raise ValidationException("学号格式错误,应为7位数字(4位年份+3位序号)")
    return True


def validate_email(email: str) -> bool:
    """验证邮箱格式
    
    Args:
        email: 邮箱地址
        
    Returns:
        bool: 是否有效
        
    Raises:
        ValidationException: 格式错误时抛出
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        raise ValidationException("邮箱格式错误")
    return True


def validate_phone(phone: str) -> bool:
    """验证手机号格式
    
    Args:
        phone: 手机号
        
    Returns:
        bool: 是否有效
        
    Raises:
        ValidationException: 格式错误时抛出
    """
    pattern = r'^1[3-9]\d{9}$'
    if not re.match(pattern, phone):
        raise ValidationException("手机号格式错误")
    return True


def validate_id_card(id_card: str) -> bool:
    """验证身份证号格式
    
    Args:
        id_card: 身份证号
        
    Returns:
        bool: 是否有效
        
    Raises:
        ValidationException: 格式错误时抛出
    """
    pattern = r'^\d{17}[\dXx]$'
    if not re.match(pattern, id_card):
        raise ValidationException("身份证号格式错误,应为18位")
    return True


def validate_score(score: float) -> bool:
    """验证成绩范围
    
    Args:
        score: 成绩
        
    Returns:
        bool: 是否有效
        
    Raises:
        ValidationException: 范围错误时抛出
    """
    if not (0 <= score <= 100):
        raise ValidationException("成绩必须在0-100之间")
    return True


def validate_age(age: int) -> bool:
    """验证年龄范围
    
    Args:
        age: 年龄
        
    Returns:
        bool: 是否有效
        
    Raises:
        ValidationException: 范围错误时抛出
    """
    if not (0 <= age <= 150):
        raise ValidationException("年龄必须在0-150之间")
    return True
