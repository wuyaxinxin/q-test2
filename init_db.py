"""数据库初始化脚本"""
from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine, Base
from app.models.user import User
from app.models.class_model import Class
from app.models.student import Student
from app.models.course import Course
from app.models.grade import Grade
from app.models.teaching import Teaching
from app.core.security import get_password_hash
from datetime import date
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init_db():
    """初始化数据库"""
    # 创建所有表
    Base.metadata.create_all(bind=engine)
    logger.info("数据库表创建成功")
    
    db = SessionLocal()
    try:
        # 检查是否已有数据
        existing_user = db.query(User).first()
        if existing_user:
            logger.info("数据库已有数据,跳过初始化")
            return
        
        # 创建管理员用户
        admin = User(
            username="admin",
            password_hash=get_password_hash("admin123"),
            email="admin@example.com",
            role="admin",
            full_name="系统管理员",
            is_active=True
        )
        db.add(admin)
        
        # 创建教师用户
        teacher = User(
            username="teacher001",
            password_hash=get_password_hash("teacher123"),
            email="teacher@example.com",
            role="teacher",
            full_name="张老师",
            is_active=True
        )
        db.add(teacher)
        
        # 创建班级
        class1 = Class(
            class_name="计算机2024-1班",
            grade_level="2024级",
            major="计算机科学与技术",
            capacity=40
        )
        db.add(class1)
        
        class2 = Class(
            class_name="软件工程2024-1班",
            grade_level="2024级",
            major="软件工程",
            capacity=40
        )
        db.add(class2)
        
        db.commit()
        db.refresh(class1)
        db.refresh(teacher)
        
        # 更新班级班主任
        class1.teacher_id = teacher.id
        
        # 创建示例学生
        students_data = [
            {"student_id": "2024001", "name": "张三", "age": 20, "gender": "male", "major": "计算机科学与技术", "class_id": class1.id},
            {"student_id": "2024002", "name": "李四", "age": 19, "gender": "female", "major": "计算机科学与技术", "class_id": class1.id},
            {"student_id": "2024003", "name": "王五", "age": 20, "gender": "male", "major": "计算机科学与技术", "class_id": class1.id},
            {"student_id": "2024004", "name": "赵六", "age": 19, "gender": "female", "major": "软件工程", "class_id": class2.id},
            {"student_id": "2024005", "name": "钱七", "age": 20, "gender": "male", "major": "软件工程", "class_id": class2.id},
        ]
        
        for student_data in students_data:
            student = Student(
                **student_data,
                enrollment_date=date(2024, 9, 1),
                status="active"
            )
            db.add(student)
        
        # 创建示例课程
        courses_data = [
            {"course_code": "CS101", "course_name": "数据结构", "credits": 4, "category": "必修", "description": "数据结构基础课程"},
            {"course_code": "CS102", "course_name": "算法设计", "credits": 3, "category": "必修", "description": "算法设计与分析"},
            {"course_code": "CS103", "course_name": "数据库原理", "credits": 3, "category": "必修", "description": "数据库系统原理"},
            {"course_code": "CS104", "course_name": "操作系统", "credits": 4, "category": "必修", "description": "操作系统原理"},
            {"course_code": "CS201", "course_name": "Web开发", "credits": 2, "category": "选修", "description": "Web应用开发"},
        ]
        
        for course_data in courses_data:
            course = Course(**course_data)
            db.add(course)
        
        db.commit()
        logger.info("示例数据初始化成功")
        
        # 显示初始账号信息
        logger.info("=" * 50)
        logger.info("初始账号信息:")
        logger.info("管理员账号: admin / admin123")
        logger.info("教师账号: teacher001 / teacher123")
        logger.info("=" * 50)
        
    except Exception as e:
        logger.error(f"初始化数据库失败: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    init_db()
