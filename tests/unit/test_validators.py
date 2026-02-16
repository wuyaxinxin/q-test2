"""验证器单元测试"""
import pytest
from app.utils.validators import (
    validate_student_id, validate_email, validate_phone,
    validate_id_card, validate_score, validate_age
)
from app.utils.exceptions import ValidationException


class TestValidators:
    """验证器测试类"""
    
    def test_validate_student_id_success(self):
        """测试有效学号"""
        assert validate_student_id("2024001") == True
        assert validate_student_id("2023999") == True
    
    def test_validate_student_id_failure(self):
        """测试无效学号"""
        with pytest.raises(ValidationException):
            validate_student_id("20240")  # 太短
        
        with pytest.raises(ValidationException):
            validate_student_id("20240012")  # 太长
        
        with pytest.raises(ValidationException):
            validate_student_id("abcd001")  # 包含字母
    
    def test_validate_email_success(self):
        """测试有效邮箱"""
        assert validate_email("test@example.com") == True
        assert validate_email("user.name@domain.co.uk") == True
    
    def test_validate_email_failure(self):
        """测试无效邮箱"""
        with pytest.raises(ValidationException):
            validate_email("invalid-email")
        
        with pytest.raises(ValidationException):
            validate_email("@example.com")
        
        with pytest.raises(ValidationException):
            validate_email("test@")
    
    def test_validate_phone_success(self):
        """测试有效手机号"""
        assert validate_phone("13800138000") == True
        assert validate_phone("15912345678") == True
    
    def test_validate_phone_failure(self):
        """测试无效手机号"""
        with pytest.raises(ValidationException):
            validate_phone("12345678901")  # 不是1开头
        
        with pytest.raises(ValidationException):
            validate_phone("1380013800")  # 太短
    
    def test_validate_id_card_success(self):
        """测试有效身份证号"""
        assert validate_id_card("110101199001011234") == True
        assert validate_id_card("11010119900101123X") == True
    
    def test_validate_id_card_failure(self):
        """测试无效身份证号"""
        with pytest.raises(ValidationException):
            validate_id_card("1101011990010112")  # 太短
        
        with pytest.raises(ValidationException):
            validate_id_card("11010119900101123A")  # 最后一位只能是数字或X
    
    def test_validate_score_success(self):
        """测试有效成绩"""
        assert validate_score(0) == True
        assert validate_score(100) == True
        assert validate_score(85.5) == True
    
    def test_validate_score_failure(self):
        """测试无效成绩"""
        with pytest.raises(ValidationException):
            validate_score(-1)
        
        with pytest.raises(ValidationException):
            validate_score(101)
    
    def test_validate_age_success(self):
        """测试有效年龄"""
        assert validate_age(0) == True
        assert validate_age(20) == True
        assert validate_age(150) == True
    
    def test_validate_age_failure(self):
        """测试无效年龄"""
        with pytest.raises(ValidationException):
            validate_age(-1)
        
        with pytest.raises(ValidationException):
            validate_age(151)
