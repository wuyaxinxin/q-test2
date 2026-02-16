"""辅助函数单元测试"""
import pytest
from app.utils.helpers import (
    calculate_gpa, get_grade_level, calculate_score_distribution,
    success_response, error_response
)


class TestHelpers:
    """辅助函数测试类"""
    
    def test_calculate_gpa(self):
        """测试GPA计算"""
        assert calculate_gpa(95) == 4.0
        assert calculate_gpa(87) == 3.7
        assert calculate_gpa(83) == 3.3
        assert calculate_gpa(80) == 3.0
        assert calculate_gpa(76) == 2.7
        assert calculate_gpa(73) == 2.3
        assert calculate_gpa(70) == 2.0
        assert calculate_gpa(65) == 1.7
        assert calculate_gpa(62) == 1.0
        assert calculate_gpa(55) == 0.0
    
    def test_get_grade_level(self):
        """测试等级获取"""
        assert get_grade_level(95) == "A"
        assert get_grade_level(87) == "A-"
        assert get_grade_level(83) == "B+"
        assert get_grade_level(80) == "B"
        assert get_grade_level(76) == "B-"
        assert get_grade_level(73) == "C+"
        assert get_grade_level(70) == "C"
        assert get_grade_level(65) == "C-"
        assert get_grade_level(62) == "D"
        assert get_grade_level(55) == "F"
    
    def test_calculate_score_distribution(self):
        """测试分数段分布计算"""
        scores = [95, 88, 76, 68, 55, 92, 81, 73, 62, 45]
        distribution = calculate_score_distribution(scores)
        
        assert distribution["excellent"] == 2  # 95, 92
        assert distribution["good"] == 2  # 88, 81
        assert distribution["medium"] == 2  # 76, 73
        assert distribution["passing"] == 2  # 68, 62
        assert distribution["failing"] == 2  # 55, 45
    
    def test_calculate_score_distribution_empty(self):
        """测试空列表的分数段分布"""
        distribution = calculate_score_distribution([])
        assert all(v == 0 for v in distribution.values())
    
    def test_success_response(self):
        """测试成功响应"""
        response = success_response({"id": 1}, "操作成功")
        assert response["code"] == 200
        assert response["message"] == "操作成功"
        assert response["data"]["id"] == 1
    
    def test_success_response_default(self):
        """测试默认成功响应"""
        response = success_response()
        assert response["code"] == 200
        assert response["message"] == "操作成功"
        assert response["data"] is None
    
    def test_error_response(self):
        """测试错误响应"""
        response = error_response("错误消息", 400, ["错误1", "错误2"])
        assert response["code"] == 400
        assert response["message"] == "错误消息"
        assert len(response["errors"]) == 2
    
    def test_error_response_no_errors(self):
        """测试无错误详情的错误响应"""
        response = error_response("错误消息", 404)
        assert response["code"] == 404
        assert response["message"] == "错误消息"
        assert "errors" not in response
