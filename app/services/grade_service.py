"""成绩服务层"""
from typing import Optional, List
from sqlalchemy.orm import Session
from app.repositories.grade_repo import GradeRepository
from app.repositories.student_repo import StudentRepository
from app.repositories.course_repo import CourseRepository
from app.schemas.grade import (
    GradeCreate, GradeUpdate, Grade, GradeList,
    GradeBatchCreate, GradeBatchResult
)
from app.utils.exceptions import ValidationException, DuplicateException, NotFoundException
from app.utils.validators import validate_score


class GradeService:
    """成绩业务逻辑类"""
    
    def __init__(self, db: Session):
        self.db = db
        self.grade_repo = GradeRepository(db)
        self.student_repo = StudentRepository(db)
        self.course_repo = CourseRepository(db)
    
    def create_grade(self, grade: GradeCreate, recorded_by: int) -> Grade:
        """录入成绩
        
        Args:
            grade: 成绩数据
            recorded_by: 录入人ID
            
        Returns:
            Grade: 创建的成绩
            
        Raises:
            ValidationException: 数据验证失败
            NotFoundException: 学生或课程不存在
            DuplicateException: 成绩已存在
        """
        # 验证分数
        validate_score(grade.score)
        
        # 检查学生是否存在
        student = self.student_repo.get_by_id(grade.student_id)
        if not student:
            raise NotFoundException(f"学生ID {grade.student_id} 不存在")
        
        # 检查课程是否存在
        course = self.course_repo.get_by_id(grade.course_id)
        if not course:
            raise NotFoundException(f"课程ID {grade.course_id} 不存在")
        
        # 检查是否已存在相同成绩记录
        existing = self.grade_repo.get_existing(
            grade.student_id,
            grade.course_id,
            grade.semester,
            grade.grade_type
        )
        if existing:
            raise DuplicateException(
                f"学生 {student.name} 在 {grade.semester} 学期的 "
                f"{course.course_name} {grade.grade_type} 成绩已存在"
            )
        
        # 创建成绩
        db_grade = self.grade_repo.create(grade, recorded_by)
        
        # 构建响应
        grade_dict = Grade.model_validate(db_grade).model_dump()
        grade_dict["student_name"] = student.name
        grade_dict["course_name"] = course.course_name
        
        return Grade(**grade_dict)
    
    def batch_create_grades(
        self,
        batch_data: GradeBatchCreate,
        recorded_by: int
    ) -> GradeBatchResult:
        """批量录入成绩
        
        Args:
            batch_data: 批量成绩数据
            recorded_by: 录入人ID
            
        Returns:
            GradeBatchResult: 录入结果
        """
        success_count = 0
        failed_items = []
        
        # 检查课程是否存在
        course = self.course_repo.get_by_id(batch_data.course_id)
        if not course:
            raise NotFoundException(f"课程ID {batch_data.course_id} 不存在")
        
        for item in batch_data.grades:
            try:
                # 创建单条成绩
                grade_data = GradeCreate(
                    student_id=item.student_id,
                    course_id=batch_data.course_id,
                    score=item.score,
                    semester=batch_data.semester,
                    academic_year=batch_data.academic_year,
                    exam_date=batch_data.exam_date,
                    grade_type=batch_data.grade_type
                )
                self.create_grade(grade_data, recorded_by)
                success_count += 1
            except Exception as e:
                failed_items.append({
                    "student_id": item.student_id,
                    "error": str(e)
                })
        
        return GradeBatchResult(
            success_count=success_count,
            failed_items=failed_items
        )
    
    def update_grade(self, grade_id: int, update_data: GradeUpdate) -> Grade:
        """更新成绩
        
        Args:
            grade_id: 成绩ID
            update_data: 更新数据
            
        Returns:
            Grade: 更新后的成绩
            
        Raises:
            NotFoundException: 成绩不存在
            ValidationException: 数据验证失败
        """
        # 验证分数
        validate_score(update_data.score)
        
        # 获取成绩
        grade = self.grade_repo.get_by_id(grade_id)
        if not grade:
            raise NotFoundException(f"成绩ID {grade_id} 不存在")
        
        # 更新成绩
        updated_grade = self.grade_repo.update(grade_id, update_data.score)
        
        # 构建响应
        grade_dict = Grade.model_validate(updated_grade).model_dump()
        grade_dict["student_name"] = updated_grade.student.name
        grade_dict["course_name"] = updated_grade.course.course_name
        
        return Grade(**grade_dict)
    
    def delete_grade(self, grade_id: int) -> bool:
        """删除成绩
        
        Args:
            grade_id: 成绩ID
            
        Returns:
            bool: 是否成功
            
        Raises:
            NotFoundException: 成绩不存在
        """
        grade = self.grade_repo.get_by_id(grade_id)
        if not grade:
            raise NotFoundException(f"成绩ID {grade_id} 不存在")
        
        return self.grade_repo.delete(grade_id)
    
    def get_student_grades(
        self,
        student_id: int,
        semester: Optional[str] = None,
        academic_year: Optional[int] = None,
        course_id: Optional[int] = None
    ) -> GradeList:
        """获取学生成绩
        
        Args:
            student_id: 学生ID
            semester: 学期筛选
            academic_year: 学年筛选
            course_id: 课程筛选
            
        Returns:
            GradeList: 成绩列表
        """
        # 检查学生是否存在
        student = self.student_repo.get_by_id(student_id)
        if not student:
            raise NotFoundException(f"学生ID {student_id} 不存在")
        
        # 获取成绩
        grades = self.grade_repo.get_by_student(
            student_id,
            semester,
            academic_year,
            course_id
        )
        
        # 构建响应
        items = []
        total_credits = 0
        for grade in grades:
            grade_dict = Grade.model_validate(grade).model_dump()
            grade_dict["student_name"] = grade.student.name
            grade_dict["course_name"] = grade.course.course_name
            items.append(Grade(**grade_dict))
            total_credits += grade.course.credits
        
        # 计算平均分
        average_score = self.grade_repo.calculate_average(grades) if grades else 0.0
        
        return GradeList(
            items=items,
            average_score=round(average_score, 2),
            total_credits=total_credits
        )
