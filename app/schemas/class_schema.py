"""班级数据模式"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ClassBase(BaseModel):
    """班级基础模式"""
    class_name: str = Field(..., min_length=2, max_length=50, description="班级名称")
    grade_level: str = Field(..., min_length=2, max_length=20, description="年级")
    major: str = Field(..., min_length=2, max_length=100, description="专业")
    capacity: int = Field(default=40, ge=1, le=200, description="容量")
    teacher_id: Optional[int] = Field(None, description="班主任ID")


class ClassCreate(ClassBase):
    """创建班级模式"""
    pass


class ClassUpdate(BaseModel):
    """更新班级模式"""
    class_name: Optional[str] = Field(None, min_length=2, max_length=50)
    grade_level: Optional[str] = Field(None, min_length=2, max_length=20)
    major: Optional[str] = Field(None, min_length=2, max_length=100)
    capacity: Optional[int] = Field(None, ge=1, le=200)
    teacher_id: Optional[int] = None


class ClassInDB(ClassBase):
    """数据库中的班级模式"""
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class Class(ClassInDB):
    """班级响应模式"""
    teacher_name: Optional[str] = None
    student_count: Optional[int] = 0


class ClassList(BaseModel):
    """班级列表响应模式"""
    total: int
    page: int
    size: int
    items: list[Class]
