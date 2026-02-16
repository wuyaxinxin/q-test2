"""用户数据模型"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class User(Base):
    """用户表"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    email = Column(String(100), unique=True, index=True)
    role = Column(String(20), nullable=False)  # admin, teacher, student
    full_name = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
    
    # 关系
    teaching_courses = relationship("Teaching", back_populates="teacher", foreign_keys="Teaching.teacher_id")
    recorded_grades = relationship("Grade", back_populates="recorder", foreign_keys="Grade.recorded_by")
    managed_classes = relationship("Class", back_populates="teacher", foreign_keys="Class.teacher_id")
