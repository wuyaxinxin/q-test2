"""学生服务层"""
from typing import Optional, List
from sqlalchemy.orm import Session
from app.repositories.student_repo import StudentRepository
from app.repositories.class_repo import ClassRepository
from app.schemas.student import StudentCreate, StudentUpdate, Student, StudentList
from app.utils.exceptions import ValidationException, DuplicateException, NotFoundException
from app.utils.validators import validate_student_id, validate_email, validate_phone, validate_id_card, validate_age


class StudentService:
    """学生业务逻辑类"""
    
    def __init__(self, db: Session):
        self.db = db
        self.student_repo = StudentRepository(db)
        self.class_repo = ClassRepository(db)
    
    def create_student(self, student: StudentCreate) -> Student:
        """创建学生
        
        Args:
            student: 学生创建数据
            
        Returns:
            Student: 创建的学生
            
        Raises:
            ValidationException: 数据验证失败
            DuplicateException: 数据重复
        """
        # 验证学号格式
        validate_student_id(student.student_id)
        
        # 验证年龄
        validate_age(student.age)
        
        # 验证邮箱格式(如果提供)
        if student.email:
            validate_email(student.email)
        
        # 验证手机号格式(如果提供)
        if student.phone:
            validate_phone(student.phone)
        
        # 验证身份证号(如果提供)
        if student.id_card:
            validate_id_card(student.id_card)
        
        # 检查学号是否重复
        existing = self.student_repo.get_by_student_id(student.student_id)
        if existing:
            raise DuplicateException(f"学号 {student.student_id} 已存在")
        
        # 检查邮箱是否重复(如果提供)
        if student.email:
            existing = self.student_repo.get_by_email(student.email)
            if existing:
                raise DuplicateException(f"邮箱 {student.email} 已存在")
        
        # 检查身份证号是否重复(如果提供)
        if student.id_card:
            existing = self.student_repo.get_by_id_card(student.id_card)
            if existing:
                raise DuplicateException(f"身份证号 {student.id_card} 已存在")
        
        # 验证班级是否存在(如果提供)
        if student.class_id:
            class_obj = self.class_repo.get_by_id(student.class_id)
            if not class_obj:
                raise NotFoundException(f"班级ID {student.class_id} 不存在")
            
            # 检查班级容量
            current_count = self.student_repo.count_by_class(student.class_id)
            if current_count >= class_obj.capacity:
                raise ValidationException(f"班级 {class_obj.class_name} 已满")
        
        # 创建学生
        db_student = self.student_repo.create(student)
        
        # 构建响应
        student_dict = Student.model_validate(db_student).model_dump()
        if db_student.class_info:
            student_dict["class_name"] = db_student.class_info.class_name
        
        return Student(**student_dict)
    
    def get_student(self, student_id: str) -> Student:
        """获取学生详情
        
        Args:
            student_id: 学号
            
        Returns:
            Student: 学生信息
            
        Raises:
            NotFoundException: 学生不存在
        """
        student = self.student_repo.get_by_student_id(student_id)
        if not student:
            raise NotFoundException(f"学号 {student_id} 不存在")
        
        student_dict = Student.model_validate(student).model_dump()
        if student.class_info:
            student_dict["class_name"] = student.class_info.class_name
        
        return Student(**student_dict)
    
    def update_student(self, student_id: str, update_data: StudentUpdate) -> Student:
        """更新学生信息
        
        Args:
            student_id: 学号
            update_data: 更新数据
            
        Returns:
            Student: 更新后的学生
            
        Raises:
            NotFoundException: 学生不存在
            ValidationException: 数据验证失败
        """
        # 获取学生
        student = self.student_repo.get_by_student_id(student_id)
        if not student:
            raise NotFoundException(f"学号 {student_id} 不存在")
        
        # 验证数据
        if update_data.age is not None:
            validate_age(update_data.age)
        
        if update_data.email is not None:
            validate_email(update_data.email)
        
        if update_data.phone is not None:
            validate_phone(update_data.phone)
        
        # 验证班级
        if update_data.class_id is not None:
            class_obj = self.class_repo.get_by_id(update_data.class_id)
            if not class_obj:
                raise NotFoundException(f"班级ID {update_data.class_id} 不存在")
        
        # 更新学生
        updated_student = self.student_repo.update(student.id, update_data)
        
        student_dict = Student.model_validate(updated_student).model_dump()
        if updated_student.class_info:
            student_dict["class_name"] = updated_student.class_info.class_name
        
        return Student(**student_dict)
    
    def delete_student(self, student_id: str) -> bool:
        """删除学生(逻辑删除)
        
        Args:
            student_id: 学号
            
        Returns:
            bool: 是否成功
            
        Raises:
            NotFoundException: 学生不存在
        """
        student = self.student_repo.get_by_student_id(student_id)
        if not student:
            raise NotFoundException(f"学号 {student_id} 不存在")
        
        return self.student_repo.delete(student.id)
    
    def get_student_list(
        self,
        page: int = 1,
        size: int = 20,
        name: Optional[str] = None,
        class_id: Optional[int] = None,
        major: Optional[str] = None,
        status: Optional[str] = None
    ) -> StudentList:
        """获取学生列表
        
        Args:
            page: 页码
            size: 每页大小
            name: 姓名筛选
            class_id: 班级ID筛选
            major: 专业筛选
            status: 状态筛选
            
        Returns:
            StudentList: 学生列表
        """
        skip = (page - 1) * size
        students, total = self.student_repo.get_list(
            skip=skip,
            limit=size,
            name=name,
            class_id=class_id,
            major=major,
            status=status
        )
        
        items = []
        for student in students:
            student_dict = Student.model_validate(student).model_dump()
            if student.class_info:
                student_dict["class_name"] = student.class_info.class_name
            items.append(Student(**student_dict))
        
        return StudentList(
            total=total,
            page=page,
            size=size,
            items=items
        )
