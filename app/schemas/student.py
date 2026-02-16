"""学生数据模式"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import date, datetime
from enum import Enum


class Gender(str, Enum):
    """性别枚举"""
    MALE = "male"
    FEMALE = "female"


class StudentStatus(str, Enum):
    """学生状态枚举"""
    ACTIVE = "active"
    GRADUATED = "graduated"
    SUSPENDED = "suspended"


class StudentBase(BaseModel):
    """学生基础模式"""
    student_id: str = Field(..., min_length=7, max_length=20, description="学号")
    name: str = Field(..., min_length=2, max_length=100, description="姓名")
    age: int = Field(..., ge=0, le=150, description="年龄")
    gender: Gender = Field(..., description="性别")
    major: str = Field(..., min_length=2, max_length=100, description="专业")
    class_id: Optional[int] = Field(None, description="班级ID")
    phone: Optional[str] = Field(None, max_length=20, description="联系电话")
    email: Optional[EmailStr] = Field(None, description="电子邮箱")
    id_card: Optional[str] = Field(None, min_length=18, max_length=18, description="身份证号")
    enrollment_date: date = Field(..., description="入学日期")
    address: Optional[str] = Field(None, description="家庭住址")


class StudentCreate(StudentBase):
    """创建学生模式"""
    pass


class StudentUpdate(BaseModel):
    """更新学生模式"""
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    age: Optional[int] = Field(None, ge=0, le=150)
    phone: Optional[str] = Field(None, max_length=20)
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    class_id: Optional[int] = None
    status: Optional[StudentStatus] = None


class StudentInDB(StudentBase):
    """数据库中的学生模式"""
    id: int
    status: StudentStatus
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class Student(StudentInDB):
    """学生响应模式"""
    class_name: Optional[str] = None


class StudentList(BaseModel):
    """学生列表响应模式"""
    total: int
    page: int
    size: int
    items: list[Student]
