"""测试配置"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.core.database import Base, get_db
from app.models.user import User
from app.models.student import Student
from app.models.class_model import Class
from app.models.course import Course
from app.core.security import get_password_hash
from main import app
from datetime import date

# 使用内存数据库进行测试
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    """数据库会话fixture"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):
    """测试客户端fixture"""
    def override_get_db():
        try:
            yield db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def test_admin(db):
    """测试管理员用户"""
    admin = User(
        username="admin",
        password_hash=get_password_hash("admin123"),
        email="admin@test.com",
        role="admin",
        full_name="测试管理员",
        is_active=True
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)
    return admin


@pytest.fixture
def test_teacher(db):
    """测试教师用户"""
    teacher = User(
        username="teacher",
        password_hash=get_password_hash("teacher123"),
        email="teacher@test.com",
        role="teacher",
        full_name="测试教师",
        is_active=True
    )
    db.add(teacher)
    db.commit()
    db.refresh(teacher)
    return teacher


@pytest.fixture
def test_class(db):
    """测试班级"""
    test_class = Class(
        class_name="测试班级",
        grade_level="2024级",
        major="计算机科学",
        capacity=40
    )
    db.add(test_class)
    db.commit()
    db.refresh(test_class)
    return test_class


@pytest.fixture
def test_student(db, test_class):
    """测试学生"""
    student = Student(
        student_id="2024001",
        name="测试学生",
        age=20,
        gender="male",
        major="计算机科学",
        class_id=test_class.id,
        enrollment_date=date(2024, 9, 1),
        status="active"
    )
    db.add(student)
    db.commit()
    db.refresh(student)
    return student


@pytest.fixture
def test_course(db):
    """测试课程"""
    course = Course(
        course_code="TEST101",
        course_name="测试课程",
        credits=3,
        category="必修",
        description="测试用课程"
    )
    db.add(course)
    db.commit()
    db.refresh(course)
    return course
