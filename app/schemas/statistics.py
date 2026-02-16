"""统计数据模式"""
from pydantic import BaseModel
from typing import Optional, Dict


class StudentStatistics(BaseModel):
    """学生成绩统计"""
    average_score: float
    highest_score: float
    lowest_score: float
    passing_rate: float
    total_credits: int
    gpa: float


class ClassStatistics(BaseModel):
    """班级成绩统计"""
    average_score: float
    highest_score: float
    lowest_score: float
    passing_rate: float
    score_distribution: Dict[str, int]  # 分数段分布


class CourseStatistics(BaseModel):
    """课程成绩统计"""
    average_score: float
    passing_rate: float
    excellent_rate: float
    score_distribution: Dict[str, int]  # 分数段分布


class ApiResponse(BaseModel):
    """统一API响应模式"""
    code: int = 200
    message: str = "操作成功"
    data: Optional[dict] = None
