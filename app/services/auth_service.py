"""认证服务层"""
from typing import Optional
from datetime import timedelta
from sqlalchemy.orm import Session
from app.repositories.user_repo import UserRepository
from app.schemas.user import UserLogin, Token, UserCreate, User, PasswordChange
from app.core.security import (
    verify_password, create_access_token, create_refresh_token,
    decode_token, get_password_hash
)
from app.core.config import settings
from app.utils.exceptions import AuthenticationException, NotFoundException, ValidationException


class AuthService:
    """认证业务逻辑类"""
    
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)
    
    def login(self, credentials: UserLogin) -> Token:
        """用户登录
        
        Args:
            credentials: 登录凭据
            
        Returns:
            Token: 访问令牌
            
        Raises:
            AuthenticationException: 认证失败
        """
        # 获取用户
        user = self.user_repo.get_by_username(credentials.username)
        if not user:
            raise AuthenticationException("用户名或密码错误")
        
        # 验证密码
        if not verify_password(credentials.password, user.password_hash):
            raise AuthenticationException("用户名或密码错误")
        
        # 检查用户是否激活
        if not user.is_active:
            raise AuthenticationException("账号已被禁用")
        
        # 创建令牌
        token_data = {
            "sub": user.username,
            "user_id": user.id,
            "role": user.role
        }
        
        access_token = create_access_token(token_data)
        refresh_token = create_refresh_token({"sub": user.username})
        
        return Token(
            access_token=access_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            refresh_token=refresh_token
        )
    
    def refresh_token(self, refresh_token: str) -> Token:
        """刷新访问令牌
        
        Args:
            refresh_token: 刷新令牌
            
        Returns:
            Token: 新的访问令牌
            
        Raises:
            AuthenticationException: 令牌无效
        """
        # 解码令牌
        payload = decode_token(refresh_token)
        if not payload or payload.get("type") != "refresh":
            raise AuthenticationException("无效的刷新令牌")
        
        # 获取用户
        username = payload.get("sub")
        user = self.user_repo.get_by_username(username)
        if not user or not user.is_active:
            raise AuthenticationException("用户不存在或已被禁用")
        
        # 创建新的访问令牌
        token_data = {
            "sub": user.username,
            "user_id": user.id,
            "role": user.role
        }
        
        access_token = create_access_token(token_data)
        
        return Token(
            access_token=access_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )
    
    def get_current_user(self, token: str) -> User:
        """获取当前用户
        
        Args:
            token: 访问令牌
            
        Returns:
            User: 当前用户
            
        Raises:
            AuthenticationException: 令牌无效
        """
        # 解码令牌
        payload = decode_token(token)
        if not payload or payload.get("type") != "access":
            raise AuthenticationException("无效的访问令牌")
        
        # 获取用户
        username = payload.get("sub")
        user = self.user_repo.get_by_username(username)
        if not user:
            raise AuthenticationException("用户不存在")
        
        return User.model_validate(user)
    
    def change_password(self, user_id: int, password_change: PasswordChange) -> bool:
        """修改密码
        
        Args:
            user_id: 用户ID
            password_change: 密码修改数据
            
        Returns:
            bool: 是否成功
            
        Raises:
            NotFoundException: 用户不存在
            ValidationException: 旧密码错误
        """
        # 获取用户
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise NotFoundException("用户不存在")
        
        # 验证旧密码
        if not verify_password(password_change.old_password, user.password_hash):
            raise ValidationException("旧密码错误")
        
        # 更新密码
        new_password_hash = get_password_hash(password_change.new_password)
        return self.user_repo.update_password(user_id, new_password_hash)
