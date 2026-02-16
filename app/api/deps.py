"""API依赖注入"""
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.auth_service import AuthService
from app.schemas.user import User
from app.utils.exceptions import AuthenticationException, PermissionException

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """获取当前登录用户
    
    Args:
        credentials: HTTP认证凭据
        db: 数据库会话
        
    Returns:
        User: 当前用户
        
    Raises:
        HTTPException: 认证失败
    """
    try:
        token = credentials.credentials
        auth_service = AuthService(db)
        user = auth_service.get_current_user(token)
        return user
    except AuthenticationException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.message,
            headers={"WWW-Authenticate": "Bearer"}
        )


def require_role(*allowed_roles: str):
    """角色权限验证装饰器
    
    Args:
        *allowed_roles: 允许的角色列表
        
    Returns:
        验证函数
    """
    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="权限不足"
            )
        return current_user
    
    return role_checker


# 预定义的角色依赖
def require_admin(current_user: User = Depends(get_current_user)) -> User:
    """要求管理员权限"""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="需要管理员权限"
        )
    return current_user


def require_teacher_or_admin(current_user: User = Depends(get_current_user)) -> User:
    """要求教师或管理员权限"""
    if current_user.role not in ["admin", "teacher"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="需要教师或管理员权限"
        )
    return current_user
