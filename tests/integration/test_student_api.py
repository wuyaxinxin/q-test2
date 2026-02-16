"""学生API集成测试"""
import pytest
from fastapi import status
from datetime import date


class TestStudentAPI:
    """学生API测试类"""
    
    def get_admin_token(self, client, test_admin):
        """获取管理员token"""
        response = client.post(
            "/api/v1/auth/login",
            json={"username": "admin", "password": "admin123"}
        )
        return response.json()["access_token"]
    
    def test_create_student_success(self, client, test_admin, test_class):
        """测试创建学生成功"""
        token = self.get_admin_token(client, test_admin)
        
        student_data = {
            "student_id": "2024999",
            "name": "测试学生",
            "age": 20,
            "gender": "male",
            "major": "计算机科学",
            "class_id": test_class.id,
            "enrollment_date": "2024-09-01"
        }
        
        response = client.post(
            "/api/v1/students",
            json=student_data,
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["student_id"] == "2024999"
        assert data["name"] == "测试学生"
    
    def test_create_student_duplicate(self, client, test_admin, test_student):
        """测试创建重复学号的学生"""
        token = self.get_admin_token(client, test_admin)
        
        student_data = {
            "student_id": test_student.student_id,  # 重复学号
            "name": "另一个学生",
            "age": 20,
            "gender": "male",
            "major": "计算机科学",
            "enrollment_date": "2024-09-01"
        }
        
        response = client.post(
            "/api/v1/students",
            json=student_data,
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == status.HTTP_409_CONFLICT
    
    def test_get_student_success(self, client, test_admin, test_student):
        """测试获取学生详情成功"""
        token = self.get_admin_token(client, test_admin)
        
        response = client.get(
            f"/api/v1/students/{test_student.student_id}",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["student_id"] == test_student.student_id
        assert data["name"] == test_student.name
    
    def test_get_student_not_found(self, client, test_admin):
        """测试获取不存在的学生"""
        token = self.get_admin_token(client, test_admin)
        
        response = client.get(
            "/api/v1/students/9999999",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_update_student_success(self, client, test_admin, test_student):
        """测试更新学生信息成功"""
        token = self.get_admin_token(client, test_admin)
        
        update_data = {
            "name": "更新后的名字",
            "age": 21
        }
        
        response = client.put(
            f"/api/v1/students/{test_student.student_id}",
            json=update_data,
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["name"] == "更新后的名字"
        assert data["age"] == 21
    
    def test_delete_student_success(self, client, test_admin, test_student):
        """测试删除学生成功"""
        token = self.get_admin_token(client, test_admin)
        
        response = client.delete(
            f"/api/v1/students/{test_student.student_id}",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == status.HTTP_200_OK
    
    def test_get_students_list(self, client, test_admin, test_student):
        """测试获取学生列表"""
        token = self.get_admin_token(client, test_admin)
        
        response = client.get(
            "/api/v1/students?page=1&size=10",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "total" in data
        assert "items" in data
        assert data["page"] == 1
        assert data["size"] == 10
