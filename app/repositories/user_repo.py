"""用户仓储层"""
from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash


class UserRepository:
    """用户数据访问类"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, user_id: int) -> Optional[User]:
        """根据ID获取用户"""
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_by_username(self, username: str) -> Optional[User]:
        """根据用户名获取用户"""
        return self.db.query(User).filter(User.username == username).first()
    
    def get_by_email(self, email: str) -> Optional[User]:
        """根据邮箱获取用户"""
        return self.db.query(User).filter(User.email == email).first()
    
    def create(self, user: UserCreate) -> User:
        """创建用户"""
        db_user = User(
            username=user.username,
            email=user.email,
            password_hash=get_password_hash(user.password),
            full_name=user.full_name,
            role=user.role.value
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def update(self, user_id: int, update_data: dict) -> Optional[User]:
        """更新用户"""
        user = self.get_by_id(user_id)
        if not user:
            return None
        
        for key, value in update_data.items():
            if value is not None:
                setattr(user, key, value)
        
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def update_password(self, user_id: int, new_password_hash: str) -> bool:
        """更新用户密码"""
        user = self.get_by_id(user_id)
        if not user:
            return False
        
        user.password_hash = new_password_hash
        self.db.commit()
        return True
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        """获取所有用户"""
        return self.db.query(User).offset(skip).limit(limit).all()
