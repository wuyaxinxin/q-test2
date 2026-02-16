"""统计服务层"""
from typing import Dict
from sqlalchemy.orm import Session
from app.repositories.grade_repo import GradeRepository
from app.repositories.student_repo import StudentRepository
from app.repositories.course_repo import CourseRepository
from app.schemas.statistics import StudentStatistics, ClassStatistics, CourseStatistics
from app.utils.exceptions import NotFoundException
from app.utils.helpers import calculate_gpa, calculate_score_distribution


class StatisticsService:
    """统计分析业务逻辑类"""
    
    def __init__(self, db: Session):
        self.db = db
        self.grade_repo = GradeRepository(db)
        self.student_repo = StudentRepository(db)
        self.course_repo = CourseRepository(db)
    
    def get_student_statistics(
        self,
        student_id: int,
        semester: str = None,
        academic_year: int = None
    ) -> StudentStatistics:
        """获取学生成绩统计
        
        Args:
            student_id: 学生ID
            semester: 学期筛选
            academic_year: 学年筛选
            
        Returns:
            StudentStatistics: 学生统计数据
            
        Raises:
            NotFoundException: 学生不存在
        """
        # 检查学生是否存在
        student = self.student_repo.get_by_id(student_id)
        if not student:
            raise NotFoundException(f"学生ID {student_id} 不存在")
        
        # 获取成绩
        grades = self.grade_repo.get_by_student(student_id, semester, academic_year)
        
        if not grades:
            return StudentStatistics(
                average_score=0.0,
                highest_score=0.0,
                lowest_score=0.0,
                passing_rate=0.0,
                total_credits=0,
                gpa=0.0
            )
        
        # 计算统计数据
        scores = [g.score for g in grades]
        average_score = sum(scores) / len(scores)
        passing_count = sum(1 for s in scores if s >= 60)
        
        # 计算总学分
        total_credits = sum(g.course.credits for g in grades)
        
        # 计算加权GPA
        total_gpa_credits = sum(calculate_gpa(g.score) * g.course.credits for g in grades)
        gpa = total_gpa_credits / total_credits if total_credits > 0 else 0.0
        
        return StudentStatistics(
            average_score=round(average_score, 2),
            highest_score=max(scores),
            lowest_score=min(scores),
            passing_rate=round(passing_count / len(scores) * 100, 2),
            total_credits=total_credits,
            gpa=round(gpa, 2)
        )
    
    def get_class_statistics(
        self,
        class_id: int,
        semester: str = None,
        course_id: int = None
    ) -> ClassStatistics:
        """获取班级成绩统计
        
        Args:
            class_id: 班级ID
            semester: 学期筛选
            course_id: 课程筛选
            
        Returns:
            ClassStatistics: 班级统计数据
        """
        # 获取班级成绩
        grades = self.grade_repo.get_by_class(class_id, semester, course_id)
        
        if not grades:
            return ClassStatistics(
                average_score=0.0,
                highest_score=0.0,
                lowest_score=0.0,
                passing_rate=0.0,
                score_distribution={}
            )
        
        # 计算统计数据
        scores = [g.score for g in grades]
        average_score = sum(scores) / len(scores)
        passing_count = sum(1 for s in scores if s >= 60)
        
        # 计算分数段分布
        distribution = calculate_score_distribution(scores)
        
        return ClassStatistics(
            average_score=round(average_score, 2),
            highest_score=max(scores),
            lowest_score=min(scores),
            passing_rate=round(passing_count / len(scores) * 100, 2),
            score_distribution=distribution
        )
    
    def get_course_statistics(
        self,
        course_id: int,
        semester: str = None,
        academic_year: int = None
    ) -> CourseStatistics:
        """获取课程成绩统计
        
        Args:
            course_id: 课程ID
            semester: 学期筛选
            academic_year: 学年筛选
            
        Returns:
            CourseStatistics: 课程统计数据
            
        Raises:
            NotFoundException: 课程不存在
        """
        # 检查课程是否存在
        course = self.course_repo.get_by_id(course_id)
        if not course:
            raise NotFoundException(f"课程ID {course_id} 不存在")
        
        # 获取课程成绩
        grades = self.grade_repo.get_by_course(course_id, semester, academic_year)
        
        if not grades:
            return CourseStatistics(
                average_score=0.0,
                passing_rate=0.0,
                excellent_rate=0.0,
                score_distribution={}
            )
        
        # 计算统计数据
        scores = [g.score for g in grades]
        average_score = sum(scores) / len(scores)
        passing_count = sum(1 for s in scores if s >= 60)
        excellent_count = sum(1 for s in scores if s >= 90)
        
        # 计算分数段分布
        distribution = calculate_score_distribution(scores)
        
        return CourseStatistics(
            average_score=round(average_score, 2),
            passing_rate=round(passing_count / len(scores) * 100, 2),
            excellent_rate=round(excellent_count / len(scores) * 100, 2),
            score_distribution=distribution
        )
