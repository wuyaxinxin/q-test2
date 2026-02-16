"""认证API集成测试"""
import pytest
from fastapi import status


class TestAuthAPI:
    """认证API测试类"""
    
    def test_login_success(self, client, test_admin):
        """测试登录成功"""
        response = client.post(
            "/api/v1/auth/login",
            json={"username": "admin", "password": "admin123"}
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"
    
    def test_login_invalid_credentials(self, client, test_admin):
        """测试登录失败 - 错误密码"""
        response = client.post(
            "/api/v1/auth/login",
            json={"username": "admin", "password": "wrongpassword"}
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_login_user_not_found(self, client):
        """测试登录失败 - 用户不存在"""
        response = client.post(
            "/api/v1/auth/login",
            json={"username": "nonexistent", "password": "password"}
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_get_current_user(self, client, test_admin):
        """测试获取当前用户信息"""
        # 先登录获取token
        login_response = client.post(
            "/api/v1/auth/login",
            json={"username": "admin", "password": "admin123"}
        )
        token = login_response.json()["access_token"]
        
        # 使用token获取用户信息
        response = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["username"] == "admin"
        assert data["role"] == "admin"
    
    def test_change_password_success(self, client, test_admin):
        """测试修改密码成功"""
        # 先登录
        login_response = client.post(
            "/api/v1/auth/login",
            json={"username": "admin", "password": "admin123"}
        )
        token = login_response.json()["access_token"]
        
        # 修改密码
        response = client.put(
            "/api/v1/auth/password",
            json={"old_password": "admin123", "new_password": "newpassword123"},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == status.HTTP_200_OK
        
        # 用新密码登录
        new_login = client.post(
            "/api/v1/auth/login",
            json={"username": "admin", "password": "newpassword123"}
        )
        assert new_login.status_code == status.HTTP_200_OK
    
    def test_change_password_wrong_old_password(self, client, test_admin):
        """测试修改密码失败 - 旧密码错误"""
        login_response = client.post(
            "/api/v1/auth/login",
            json={"username": "admin", "password": "admin123"}
        )
        token = login_response.json()["access_token"]
        
        response = client.put(
            "/api/v1/auth/password",
            json={"old_password": "wrongpassword", "new_password": "newpassword123"},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
