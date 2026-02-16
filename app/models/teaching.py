"""授课数据模型"""
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class Teaching(Base):
    """授课表"""
    __tablename__ = "teachings"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False, index=True)
    teacher_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    semester = Column(String(20), nullable=False)  # 学期
    academic_year = Column(Integer, nullable=False)  # 学年
    classroom = Column(String(50))  # 教室
    schedule = Column(String(200))  # 上课时间
    
    # 关系
    course = relationship("Course", back_populates="teachings")
    teacher = relationship("User", back_populates="teaching_courses", foreign_keys=[teacher_id])
