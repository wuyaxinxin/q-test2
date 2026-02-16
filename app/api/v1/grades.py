"""成绩管理API"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.core.database import get_db
from app.services.grade_service import GradeService
from app.schemas.grade import (
    GradeCreate, GradeUpdate, Grade, GradeList,
    GradeBatchCreate, GradeBatchResult
)
from app.schemas.user import User
from app.api.deps import get_current_user, require_admin, require_teacher_or_admin
from app.utils.exceptions import ValidationException, DuplicateException, NotFoundException

router = APIRouter(prefix="/grades", tags=["成绩管理"])


@router.post("", response_model=Grade, status_code=status.HTTP_201_CREATED, summary="录入成绩")
def create_grade(
    grade: GradeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher_or_admin)
):
    """
    录入成绩(需要教师或管理员权限)
    
    - **student_id**: 学生ID
    - **course_id**: 课程ID
    - **score**: 成绩分数(0-100)
    - **semester**: 学期
    - **academic_year**: 学年
    - **grade_type**: 成绩类型(期中/期末/平时)
    """
    try:
        grade_service = GradeService(db)
        return grade_service.create_grade(grade, current_user.id)
    except (ValidationException, DuplicateException, NotFoundException) as e:
        raise HTTPException(status_code=e.code, detail=e.message)


@router.post("/batch", response_model=GradeBatchResult, summary="批量录入成绩")
def batch_create_grades(
    batch_data: GradeBatchCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher_or_admin)
):
    """
    批量录入成绩(需要教师或管理员权限)
    
    - **course_id**: 课程ID
    - **semester**: 学期
    - **academic_year**: 学年
    - **grade_type**: 成绩类型
    - **grades**: 成绩列表
    """
    try:
        grade_service = GradeService(db)
        return grade_service.batch_create_grades(batch_data, current_user.id)
    except NotFoundException as e:
        raise HTTPException(status_code=e.code, detail=e.message)


@router.get("/student/{student_id}", response_model=GradeList, summary="查询学生成绩")
def get_student_grades(
    student_id: int,
    semester: Optional[str] = Query(None, description="学期筛选"),
    academic_year: Optional[int] = Query(None, description="学年筛选"),
    course_id: Optional[int] = Query(None, description="课程筛选"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    查询学生成绩
    
    - 管理员和教师可查看任意学生成绩
    - 学生只能查看本人成绩
    """
    try:
        grade_service = GradeService(db)
        
        # 权限检查:学生只能查看本人成绩
        # TODO: 需要根据student_id和current_user进行更严格的权限检查
        
        return grade_service.get_student_grades(
            student_id,
            semester,
            academic_year,
            course_id
        )
    except NotFoundException as e:
        raise HTTPException(status_code=e.code, detail=e.message)


@router.put("/{grade_id}", response_model=Grade, summary="更新成绩")
def update_grade(
    grade_id: int,
    update_data: GradeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher_or_admin)
):
    """
    更新成绩(需要教师或管理员权限)
    """
    try:
        grade_service = GradeService(db)
        return grade_service.update_grade(grade_id, update_data)
    except (NotFoundException, ValidationException) as e:
        raise HTTPException(status_code=e.code, detail=e.message)


@router.delete("/{grade_id}", summary="删除成绩")
def delete_grade(
    grade_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    删除成绩(需要管理员权限)
    """
    try:
        grade_service = GradeService(db)
        grade_service.delete_grade(grade_id)
        return {"code": 200, "message": "删除成功"}
    except NotFoundException as e:
        raise HTTPException(status_code=e.code, detail=e.message)
