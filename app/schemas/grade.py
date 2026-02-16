"""成绩数据模式"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime


class GradeBase(BaseModel):
    """成绩基础模式"""
    student_id: int = Field(..., description="学生ID")
    course_id: int = Field(..., description="课程ID")
    score: float = Field(..., ge=0, le=100, description="成绩分数")
    semester: str = Field(..., min_length=2, max_length=20, description="学期")
    academic_year: int = Field(..., ge=2000, le=2100, description="学年")
    exam_date: Optional[date] = Field(None, description="考试日期")
    grade_type: str = Field(..., description="成绩类型")


class GradeCreate(GradeBase):
    """创建成绩模式"""
    pass


class GradeUpdate(BaseModel):
    """更新成绩模式"""
    score: float = Field(..., ge=0, le=100, description="成绩分数")


class GradeBatchItem(BaseModel):
    """批量成绩项"""
    student_id: int = Field(..., description="学生ID")
    score: float = Field(..., ge=0, le=100, description="成绩分数")


class GradeBatchCreate(BaseModel):
    """批量创建成绩模式"""
    course_id: int = Field(..., description="课程ID")
    semester: str = Field(..., min_length=2, max_length=20, description="学期")
    academic_year: int = Field(..., ge=2000, le=2100, description="学年")
    grade_type: str = Field(..., description="成绩类型")
    exam_date: Optional[date] = Field(None, description="考试日期")
    grades: list[GradeBatchItem] = Field(..., description="成绩列表")


class GradeInDB(GradeBase):
    """数据库中的成绩模式"""
    id: int
    recorded_at: datetime
    recorded_by: int
    
    class Config:
        from_attributes = True


class Grade(GradeInDB):
    """成绩响应模式"""
    student_name: Optional[str] = None
    course_name: Optional[str] = None
    recorder_name: Optional[str] = None


class GradeList(BaseModel):
    """成绩列表响应模式"""
    items: list[Grade]
    average_score: Optional[float] = None
    total_credits: Optional[int] = None


class GradeBatchResult(BaseModel):
    """批量成绩录入结果"""
    success_count: int
    failed_items: list[dict]
