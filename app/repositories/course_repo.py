"""课程仓储层"""
from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.course import Course
from app.schemas.course import CourseCreate, CourseUpdate


class CourseRepository:
    """课程数据访问类"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, course_id: int) -> Optional[Course]:
        """根据ID获取课程"""
        return self.db.query(Course).filter(Course.id == course_id).first()
    
    def get_by_code(self, course_code: str) -> Optional[Course]:
        """根据课程代码获取课程"""
        return self.db.query(Course).filter(Course.course_code == course_code).first()
    
    def create(self, course: CourseCreate) -> Course:
        """创建课程"""
        db_course = Course(**course.model_dump())
        self.db.add(db_course)
        self.db.commit()
        self.db.refresh(db_course)
        return db_course
    
    def update(self, course_id: int, update_data: CourseUpdate) -> Optional[Course]:
        """更新课程"""
        course = self.get_by_id(course_id)
        if not course:
            return None
        
        update_dict = update_data.model_dump(exclude_unset=True)
        for key, value in update_dict.items():
            setattr(course, key, value)
        
        self.db.commit()
        self.db.refresh(course)
        return course
    
    def delete(self, course_id: int) -> bool:
        """删除课程"""
        course = self.get_by_id(course_id)
        if not course:
            return False
        
        self.db.delete(course)
        self.db.commit()
        return True
    
    def get_list(
        self,
        skip: int = 0,
        limit: int = 100,
        category: Optional[str] = None,
        name: Optional[str] = None
    ) -> tuple[List[Course], int]:
        """获取课程列表"""
        query = self.db.query(Course)
        
        if category:
            query = query.filter(Course.category == category)
        if name:
            query = query.filter(Course.course_name.contains(name))
        
        total = query.count()
        courses = query.offset(skip).limit(limit).all()
        return courses, total
