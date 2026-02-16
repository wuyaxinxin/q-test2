"""成绩数据模型"""
from sqlalchemy import Column, Integer, Float, String, Date, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class Grade(Base):
    """成绩表"""
    __tablename__ = "grades"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False, index=True)
    score = Column(Float, nullable=False)  # 成绩分数 0-100
    semester = Column(String(20), nullable=False)  # 学期 如: 2024春
    academic_year = Column(Integer, nullable=False)  # 学年
    exam_date = Column(Date)  # 考试日期
    grade_type = Column(String(20), nullable=False)  # 成绩类型(期中/期末/平时)
    recorded_at = Column(DateTime, default=datetime.utcnow, nullable=False)  # 录入时间
    recorded_by = Column(Integer, ForeignKey("users.id"), nullable=False)  # 录入人ID
    
    # 关系
    student = relationship("Student", back_populates="grades")
    course = relationship("Course", back_populates="grades")
    recorder = relationship("User", back_populates="recorded_grades", foreign_keys=[recorded_by])
    
    # 唯一约束: 同一学生同课程同学期同类型成绩唯一
    __table_args__ = (
        UniqueConstraint('student_id', 'course_id', 'semester', 'grade_type', name='uq_student_course_semester_type'),
    )
