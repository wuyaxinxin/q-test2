"""班级数据模型"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class Class(Base):
    """班级表"""
    __tablename__ = "classes"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    class_name = Column(String(50), unique=True, nullable=False, index=True)
    grade_level = Column(String(20), nullable=False)  # 年级
    major = Column(String(100), nullable=False)  # 专业
    capacity = Column(Integer, default=40, nullable=False)  # 容量
    teacher_id = Column(Integer, ForeignKey("users.id"))  # 班主任ID
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # 关系
    students = relationship("Student", back_populates="class_info")
    teacher = relationship("User", back_populates="managed_classes", foreign_keys=[teacher_id])
