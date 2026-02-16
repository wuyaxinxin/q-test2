"""课程数据模式"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class CourseBase(BaseModel):
    """课程基础模式"""
    course_code: str = Field(..., min_length=2, max_length=20, description="课程代码")
    course_name: str = Field(..., min_length=2, max_length=100, description="课程名称")
    credits: int = Field(..., ge=1, le=10, description="学分")
    category: str = Field(..., min_length=2, max_length=50, description="课程类别")
    description: Optional[str] = Field(None, description="课程描述")
    prerequisite: Optional[str] = Field(None, max_length=100, description="先修课程")


class CourseCreate(CourseBase):
    """创建课程模式"""
    pass


class CourseUpdate(BaseModel):
    """更新课程模式"""
    course_name: Optional[str] = Field(None, min_length=2, max_length=100)
    credits: Optional[int] = Field(None, ge=1, le=10)
    category: Optional[str] = Field(None, min_length=2, max_length=50)
    description: Optional[str] = None
    prerequisite: Optional[str] = Field(None, max_length=100)


class CourseInDB(CourseBase):
    """数据库中的课程模式"""
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class Course(CourseInDB):
    """课程响应模式"""
    pass


class CourseList(BaseModel):
    """课程列表响应模式"""
    total: int
    page: int
    size: int
    items: list[Course]
