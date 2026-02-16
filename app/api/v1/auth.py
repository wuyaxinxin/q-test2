"""认证相关API"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.auth_service import AuthService
from app.schemas.user import UserLogin, Token, PasswordChange, User
from app.api.deps import get_current_user
from app.utils.exceptions import AuthenticationException, ValidationException

router = APIRouter(prefix="/auth", tags=["认证"])


@router.post("/login", response_model=Token, summary="用户登录")
def login(
    credentials: UserLogin,
    db: Session = Depends(get_db)
):
    """
    用户登录接口
    
    - **username**: 用户名
    - **password**: 密码
    """
    try:
        auth_service = AuthService(db)
        return auth_service.login(credentials)
    except AuthenticationException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.message
        )


@router.post("/refresh", response_model=Token, summary="刷新令牌")
def refresh_token(
    refresh_token: str,
    db: Session = Depends(get_db)
):
    """
    刷新访问令牌
    
    - **refresh_token**: 刷新令牌
    """
    try:
        auth_service = AuthService(db)
        return auth_service.refresh_token(refresh_token)
    except AuthenticationException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.message
        )


@router.put("/password", summary="修改密码")
def change_password(
    password_change: PasswordChange,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    修改密码
    
    - **old_password**: 旧密码
    - **new_password**: 新密码
    """
    try:
        auth_service = AuthService(db)
        auth_service.change_password(current_user.id, password_change)
        return {"code": 200, "message": "密码修改成功"}
    except ValidationException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.message
        )


@router.get("/me", response_model=User, summary="获取当前用户信息")
def get_me(current_user: User = Depends(get_current_user)):
    """
    获取当前登录用户信息
    """
    return current_user
