"""成绩仓储层"""
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from app.models.grade import Grade
from app.schemas.grade import GradeCreate


class GradeRepository:
    """成绩数据访问类"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, grade_id: int) -> Optional[Grade]:
        """根据ID获取成绩"""
        return self.db.query(Grade).filter(Grade.id == grade_id).first()
    
    def get_existing(
        self,
        student_id: int,
        course_id: int,
        semester: str,
        grade_type: str
    ) -> Optional[Grade]:
        """检查成绩是否已存在"""
        return self.db.query(Grade).filter(
            and_(
                Grade.student_id == student_id,
                Grade.course_id == course_id,
                Grade.semester == semester,
                Grade.grade_type == grade_type
            )
        ).first()
    
    def create(self, grade: GradeCreate, recorded_by: int) -> Grade:
        """创建成绩"""
        db_grade = Grade(
            **grade.model_dump(),
            recorded_by=recorded_by
        )
        self.db.add(db_grade)
        self.db.commit()
        self.db.refresh(db_grade)
        return db_grade
    
    def update(self, grade_id: int, score: float) -> Optional[Grade]:
        """更新成绩"""
        grade = self.get_by_id(grade_id)
        if not grade:
            return None
        
        grade.score = score
        self.db.commit()
        self.db.refresh(grade)
        return grade
    
    def delete(self, grade_id: int) -> bool:
        """删除成绩"""
        grade = self.get_by_id(grade_id)
        if not grade:
            return False
        
        self.db.delete(grade)
        self.db.commit()
        return True
    
    def get_by_student(
        self,
        student_id: int,
        semester: Optional[str] = None,
        academic_year: Optional[int] = None,
        course_id: Optional[int] = None
    ) -> List[Grade]:
        """获取学生成绩"""
        query = self.db.query(Grade).filter(Grade.student_id == student_id)
        
        if semester:
            query = query.filter(Grade.semester == semester)
        if academic_year:
            query = query.filter(Grade.academic_year == academic_year)
        if course_id:
            query = query.filter(Grade.course_id == course_id)
        
        return query.all()
    
    def get_by_course(
        self,
        course_id: int,
        semester: Optional[str] = None,
        academic_year: Optional[int] = None
    ) -> List[Grade]:
        """获取课程所有成绩"""
        query = self.db.query(Grade).filter(Grade.course_id == course_id)
        
        if semester:
            query = query.filter(Grade.semester == semester)
        if academic_year:
            query = query.filter(Grade.academic_year == academic_year)
        
        return query.all()
    
    def get_by_class(
        self,
        class_id: int,
        semester: Optional[str] = None,
        course_id: Optional[int] = None
    ) -> List[Grade]:
        """获取班级成绩"""
        from app.models.student import Student
        
        query = self.db.query(Grade).join(Student).filter(Student.class_id == class_id)
        
        if semester:
            query = query.filter(Grade.semester == semester)
        if course_id:
            query = query.filter(Grade.course_id == course_id)
        
        return query.all()
    
    def calculate_average(self, grades: List[Grade]) -> float:
        """计算平均分"""
        if not grades:
            return 0.0
        return sum(g.score for g in grades) / len(grades)
    
    def get_statistics(self, grades: List[Grade]) -> dict:
        """计算成绩统计信息"""
        if not grades:
            return {
                "average": 0.0,
                "highest": 0.0,
                "lowest": 0.0,
                "passing_rate": 0.0,
                "total": 0
            }
        
        scores = [g.score for g in grades]
        passing_count = sum(1 for s in scores if s >= 60)
        
        return {
            "average": sum(scores) / len(scores),
            "highest": max(scores),
            "lowest": min(scores),
            "passing_rate": passing_count / len(scores) * 100,
            "total": len(scores)
        }
