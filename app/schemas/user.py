"""用户数据模式"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class UserRole(str, Enum):
    """用户角色枚举"""
    ADMIN = "admin"
    TEACHER = "teacher"
    STUDENT = "student"


class UserBase(BaseModel):
    """用户基础模式"""
    username: str = Field(..., min_length=3, max_length=50, description="用户名")
    email: Optional[EmailStr] = Field(None, description="电子邮箱")
    full_name: str = Field(..., min_length=2, max_length=100, description="真实姓名")
    role: UserRole = Field(..., description="用户角色")


class UserCreate(UserBase):
    """创建用户模式"""
    password: str = Field(..., min_length=6, max_length=50, description="密码")


class UserUpdate(BaseModel):
    """更新用户模式"""
    email: Optional[EmailStr] = None
    full_name: Optional[str] = Field(None, min_length=2, max_length=100)
    is_active: Optional[bool] = None


class UserInDB(UserBase):
    """数据库中的用户模式"""
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class User(UserInDB):
    """用户响应模式"""
    pass


class UserLogin(BaseModel):
    """用户登录模式"""
    username: str = Field(..., description="用户名")
    password: str = Field(..., description="密码")


class Token(BaseModel):
    """令牌响应模式"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    refresh_token: Optional[str] = None


class TokenData(BaseModel):
    """令牌数据模式"""
    username: Optional[str] = None
    role: Optional[str] = None


class PasswordChange(BaseModel):
    """密码修改模式"""
    old_password: str = Field(..., description="旧密码")
    new_password: str = Field(..., min_length=6, max_length=50, description="新密码")
