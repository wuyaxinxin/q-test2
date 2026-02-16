"""课程数据模型"""
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class Course(Base):
    """课程表"""
    __tablename__ = "courses"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    course_code = Column(String(20), unique=True, nullable=False, index=True)  # 课程代码
    course_name = Column(String(100), nullable=False, index=True)  # 课程名称
    credits = Column(Integer, nullable=False)  # 学分
    category = Column(String(50), nullable=False)  # 课程类别(必修/选修)
    description = Column(Text)  # 课程描述
    prerequisite = Column(String(100))  # 先修课程
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # 关系
    grades = relationship("Grade", back_populates="course")
    teachings = relationship("Teaching", back_populates="course")
