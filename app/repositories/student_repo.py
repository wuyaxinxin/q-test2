"""学生仓储层"""
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.student import Student
from app.schemas.student import StudentCreate, StudentUpdate


class StudentRepository:
    """学生数据访问类"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, student_id: int) -> Optional[Student]:
        """根据ID获取学生"""
        return self.db.query(Student).filter(Student.id == student_id).first()
    
    def get_by_student_id(self, student_id: str) -> Optional[Student]:
        """根据学号获取学生"""
        return self.db.query(Student).filter(Student.student_id == student_id).first()
    
    def get_by_email(self, email: str) -> Optional[Student]:
        """根据邮箱获取学生"""
        return self.db.query(Student).filter(Student.email == email).first()
    
    def get_by_id_card(self, id_card: str) -> Optional[Student]:
        """根据身份证号获取学生"""
        return self.db.query(Student).filter(Student.id_card == id_card).first()
    
    def create(self, student: StudentCreate) -> Student:
        """创建学生"""
        db_student = Student(**student.model_dump())
        self.db.add(db_student)
        self.db.commit()
        self.db.refresh(db_student)
        return db_student
    
    def update(self, student_id: int, update_data: StudentUpdate) -> Optional[Student]:
        """更新学生"""
        student = self.get_by_id(student_id)
        if not student:
            return None
        
        update_dict = update_data.model_dump(exclude_unset=True)
        for key, value in update_dict.items():
            setattr(student, key, value)
        
        self.db.commit()
        self.db.refresh(student)
        return student
    
    def delete(self, student_id: int) -> bool:
        """删除学生(逻辑删除)"""
        student = self.get_by_id(student_id)
        if not student:
            return False
        
        student.status = "deleted"
        self.db.commit()
        return True
    
    def get_list(
        self,
        skip: int = 0,
        limit: int = 100,
        name: Optional[str] = None,
        class_id: Optional[int] = None,
        major: Optional[str] = None,
        status: Optional[str] = None
    ) -> tuple[List[Student], int]:
        """获取学生列表"""
        query = self.db.query(Student)
        
        if name:
            query = query.filter(Student.name.contains(name))
        if class_id:
            query = query.filter(Student.class_id == class_id)
        if major:
            query = query.filter(Student.major == major)
        if status:
            query = query.filter(Student.status == status)
        
        total = query.count()
        students = query.offset(skip).limit(limit).all()
        return students, total
    
    def get_by_class(self, class_id: int) -> List[Student]:
        """获取班级的所有学生"""
        return self.db.query(Student).filter(Student.class_id == class_id).all()
    
    def count_by_class(self, class_id: int) -> int:
        """统计班级学生数"""
        return self.db.query(Student).filter(Student.class_id == class_id).count()
