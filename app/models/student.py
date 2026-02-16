"""学生数据模型"""
from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class Student(Base):
    """学生表"""
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    student_id = Column(String(20), unique=True, nullable=False, index=True)  # 学号
    name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String(10), nullable=False)  # male, female
    major = Column(String(100), nullable=False)
    class_id = Column(Integer, ForeignKey("classes.id"))
    phone = Column(String(20))
    email = Column(String(100))
    id_card = Column(String(18), unique=True)  # 身份证号
    enrollment_date = Column(Date, nullable=False)  # 入学日期
    status = Column(String(20), default="active", nullable=False)  # active, graduated, suspended
    address = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
    
    # 关系
    class_info = relationship("Class", back_populates="students")
    grades = relationship("Grade", back_populates="student")
