"""学生管理API"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.core.database import get_db
from app.services.student_service import StudentService
from app.schemas.student import StudentCreate, StudentUpdate, Student, StudentList
from app.schemas.user import User
from app.api.deps import get_current_user, require_admin, require_teacher_or_admin
from app.utils.exceptions import ValidationException, DuplicateException, NotFoundException

router = APIRouter(prefix="/students", tags=["学生管理"])


@router.post("", response_model=Student, status_code=status.HTTP_201_CREATED, summary="创建学生")
def create_student(
    student: StudentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    创建学生(需要管理员权限)
    
    - **student_id**: 学号(7位数字)
    - **name**: 姓名
    - **age**: 年龄
    - **gender**: 性别(male/female)
    - **major**: 专业
    - **class_id**: 班级ID(可选)
    - **phone**: 联系电话(可选)
    - **email**: 电子邮箱(可选)
    - **enrollment_date**: 入学日期
    """
    try:
        student_service = StudentService(db)
        return student_service.create_student(student)
    except (ValidationException, DuplicateException, NotFoundException) as e:
        raise HTTPException(status_code=e.code, detail=e.message)


@router.get("", response_model=StudentList, summary="查询学生列表")
def get_students(
    page: int = Query(1, ge=1, description="页码"),
    size: int = Query(20, ge=1, le=100, description="每页大小"),
    name: Optional[str] = Query(None, description="姓名筛选"),
    class_id: Optional[int] = Query(None, description="班级ID筛选"),
    major: Optional[str] = Query(None, description="专业筛选"),
    status: Optional[str] = Query(None, description="状态筛选"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_teacher_or_admin)
):
    """
    查询学生列表(需要教师或管理员权限)
    
    支持分页和筛选
    """
    student_service = StudentService(db)
    return student_service.get_student_list(page, size, name, class_id, major, status)


@router.get("/{student_id}", response_model=Student, summary="查询学生详情")
def get_student(
    student_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    查询学生详情
    
    - 管理员和教师可查看任意学生
    - 学生只能查看本人信息
    """
    try:
        student_service = StudentService(db)
        student = student_service.get_student(student_id)
        
        # 权限检查:学生只能查看本人
        if current_user.role == "student" and current_user.username != student_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="只能查看本人信息"
            )
        
        return student
    except NotFoundException as e:
        raise HTTPException(status_code=e.code, detail=e.message)


@router.put("/{student_id}", response_model=Student, summary="更新学生信息")
def update_student(
    student_id: str,
    update_data: StudentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    更新学生信息(需要管理员权限)
    """
    try:
        student_service = StudentService(db)
        return student_service.update_student(student_id, update_data)
    except (NotFoundException, ValidationException) as e:
        raise HTTPException(status_code=e.code, detail=e.message)


@router.delete("/{student_id}", summary="删除学生")
def delete_student(
    student_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    删除学生(逻辑删除,需要管理员权限)
    """
    try:
        student_service = StudentService(db)
        student_service.delete_student(student_id)
        return {"code": 200, "message": "删除成功"}
    except NotFoundException as e:
        raise HTTPException(status_code=e.code, detail=e.message)
