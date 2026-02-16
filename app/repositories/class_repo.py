"""班级仓储层"""
from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.class_model import Class
from app.schemas.class_schema import ClassCreate, ClassUpdate


class ClassRepository:
    """班级数据访问类"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, class_id: int) -> Optional[Class]:
        """根据ID获取班级"""
        return self.db.query(Class).filter(Class.id == class_id).first()
    
    def get_by_name(self, class_name: str) -> Optional[Class]:
        """根据班级名称获取班级"""
        return self.db.query(Class).filter(Class.class_name == class_name).first()
    
    def create(self, class_data: ClassCreate) -> Class:
        """创建班级"""
        db_class = Class(**class_data.model_dump())
        self.db.add(db_class)
        self.db.commit()
        self.db.refresh(db_class)
        return db_class
    
    def update(self, class_id: int, update_data: ClassUpdate) -> Optional[Class]:
        """更新班级"""
        class_obj = self.get_by_id(class_id)
        if not class_obj:
            return None
        
        update_dict = update_data.model_dump(exclude_unset=True)
        for key, value in update_dict.items():
            setattr(class_obj, key, value)
        
        self.db.commit()
        self.db.refresh(class_obj)
        return class_obj
    
    def delete(self, class_id: int) -> bool:
        """删除班级"""
        class_obj = self.get_by_id(class_id)
        if not class_obj:
            return False
        
        self.db.delete(class_obj)
        self.db.commit()
        return True
    
    def get_list(
        self,
        skip: int = 0,
        limit: int = 100,
        grade_level: Optional[str] = None,
        major: Optional[str] = None
    ) -> tuple[List[Class], int]:
        """获取班级列表"""
        query = self.db.query(Class)
        
        if grade_level:
            query = query.filter(Class.grade_level == grade_level)
        if major:
            query = query.filter(Class.major == major)
        
        total = query.count()
        classes = query.offset(skip).limit(limit).all()
        return classes, total
