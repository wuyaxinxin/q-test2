"""统计分析API"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.core.database import get_db
from app.services.statistics_service import StatisticsService
from app.schemas.statistics import StudentStatistics, ClassStatistics, CourseStatistics
from app.schemas.user import User
from app.api.deps import get_current_user, require_teacher_or_admin
from app.utils.exceptions import NotFoundException

router = APIRouter(prefix="/statistics", tags=["统计分析"])


@router.get("/student/{student_id}", response_model=StudentStatistics, summary="学生成绩统计")
def get_student_statistics(
    student_id: int,
    semester: Optional[str] = Query(None, description="学期筛选"),
    academic_year: Optional[int] = Query(None, description="学年筛选"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取学生成绩统计
    
    返回平均分、最高分、最低分、及格率、总学分、GPA等信息
    """
    try:
        statistics_service = StatisticsService(db)
        return statistics_service.get_student_statistics(
            student_id,
            semester,
            academic_year
        )
    except NotFoundException as e:
        raise HTTPException(status_code=e.code, detail=e.message)


@router.get("/class/{class_id}", response_model=ClassStatistics, summary="班级成绩统计")
def get_class_statistics(
    class_id: int,
    semester: Optional[str] = Query(None, description="学期筛选"),
    course_id: Optional[int] = Query(None, description="课程筛选"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher_or_admin)
):
    """
    获取班级成绩统计(需要教师或管理员权限)
    
    返回平均分、最高分、最低分、及格率、分数段分布等信息
    """
    statistics_service = StatisticsService(db)
    return statistics_service.get_class_statistics(
        class_id,
        semester,
        course_id
    )


@router.get("/course/{course_id}", response_model=CourseStatistics, summary="课程成绩统计")
def get_course_statistics(
    course_id: int,
    semester: Optional[str] = Query(None, description="学期筛选"),
    academic_year: Optional[int] = Query(None, description="学年筛选"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher_or_admin)
):
    """
    获取课程成绩统计(需要教师或管理员权限)
    
    返回平均分、及格率、优秀率、分数段分布等信息
    """
    try:
        statistics_service = StatisticsService(db)
        return statistics_service.get_course_statistics(
            course_id,
            semester,
            academic_year
        )
    except NotFoundException as e:
        raise HTTPException(status_code=e.code, detail=e.message)
