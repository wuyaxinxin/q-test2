#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
文件名: course.py
作者: 开发者
创建日期: 2025-10-11
版本: 1.0
描述: 课程信息管理的Python类文件
      包含课程的基本信息管理和选课管理功能
功能:
  - 课程基本信息管理（课程名称、代码、学分、学时）
  - 学生选课管理
  - 课程统计信息
  - 课程容量管理
依赖: 无外部依赖，仅使用Python标准库
使用示例:
  course = Course("数据结构", "CS201", 4, 64)
  course.set_capacity(50)
  course.enroll_student("2021001")
  print(course.get_course_info())
修改记录:
  2025-10-11 - 初始版本创建
"""

from typing import List, Dict, Optional, Set
from datetime import datetime, time
from enum import Enum


class CourseType(Enum):
    """课程类型枚举"""
    REQUIRED = "必修课"
    ELECTIVE = "选修课"
    PUBLIC = "公共课"
    PROFESSIONAL = "专业课"


class CourseStatus(Enum):
    """课程状态枚举"""
    PLANNING = "筹划中"
    OPEN = "开放选课"
    IN_PROGRESS = "进行中"
    COMPLETED = "已结课"
    CANCELLED = "已取消"


class Course:
    """课程类 - 管理课程的基本信息和选课信息"""
    
    def __init__(self, name: str, course_code: str, credits: float, hours: int):
        """
        初始化课程对象
        
        Args:
            name (str): 课程名称
            course_code (str): 课程代码
            credits (float): 学分
            hours (int): 总学时
        """
        self.name = name
        self.course_code = course_code
        self.credits = credits
        self.hours = hours
        self.enrolled_students: Set[str] = set()  # 已选课学生学号集合
        self.capacity = 0  # 课程容量，0表示无限制
        self.teacher_id: Optional[str] = None  # 授课教师工号
        self.course_type = CourseType.REQUIRED
        self.status = CourseStatus.PLANNING
        self.description = ""
        self.prerequisites: List[str] = []  # 先修课程代码列表
        self.created_time = datetime.now()
        self.semester = ""  # 学期，如"2025-春季"
        self.classroom = ""  # 教室
        self.schedule: List[Dict[str, str]] = []  # 上课时间安排
    
    def set_capacity(self, capacity: int) -> None:
        """
        设置课程容量
        
        Args:
            capacity (int): 课程容量，0表示无限制
        """
        self.capacity = max(0, capacity)
        print(f"课程容量已设置为: {self.capacity if self.capacity > 0 else '不限'}")
    
    def set_teacher(self, teacher_id: str) -> None:
        """
        设置授课教师
        
        Args:
            teacher_id (str): 教师工号
        """
        self.teacher_id = teacher_id
        print(f"授课教师已设置: {teacher_id}")
    
    def set_course_type(self, course_type: CourseType) -> None:
        """
        设置课程类型
        
        Args:
            course_type (CourseType): 课程类型
        """
        self.course_type = course_type
        print(f"课程类型已设置为: {course_type.value}")
    
    def set_status(self, status: CourseStatus) -> None:
        """
        设置课程状态
        
        Args:
            status (CourseStatus): 课程状态
        """
        self.status = status
        print(f"课程状态已更新为: {status.value}")
    
    def set_description(self, description: str) -> None:
        """
        设置课程描述
        
        Args:
            description (str): 课程描述
        """
        self.description = description
    
    def add_prerequisite(self, course_code: str) -> bool:
        """
        添加先修课程
        
        Args:
            course_code (str): 先修课程代码
            
        Returns:
            bool: 添加成功返回True，已存在返回False
        """
        if course_code in self.prerequisites:
            print(f"警告：先修课程 {course_code} 已存在")
            return False
        
        self.prerequisites.append(course_code)
        print(f"成功添加先修课程: {course_code}")
        return True
    
    def set_semester(self, semester: str) -> None:
        """
        设置开课学期
        
        Args:
            semester (str): 学期，如"2025-春季"
        """
        self.semester = semester
        print(f"开课学期已设置为: {semester}")
    
    def set_classroom(self, classroom: str) -> None:
        """
        设置上课教室
        
        Args:
            classroom (str): 教室
        """
        self.classroom = classroom
        print(f"上课教室已设置为: {classroom}")
    
    def add_schedule(self, weekday: str, start_time: str, end_time: str) -> None:
        """
        添加上课时间
        
        Args:
            weekday (str): 星期几（如：周一）
            start_time (str): 开始时间（如：08:00）
            end_time (str): 结束时间（如：09:40）
        """
        schedule_item = {
            "weekday": weekday,
            "start_time": start_time,
            "end_time": end_time
        }
        self.schedule.append(schedule_item)
        print(f"成功添加上课时间: {weekday} {start_time}-{end_time}")
    
    def is_full(self) -> bool:
        """
        检查课程是否已满
        
        Returns:
            bool: 课程已满返回True，否则返回False
        """
        if self.capacity == 0:
            return False
        return len(self.enrolled_students) >= self.capacity
    
    def get_available_seats(self) -> Optional[int]:
        """
        获取剩余名额
        
        Returns:
            Optional[int]: 剩余名额，容量不限时返回None
        """
        if self.capacity == 0:
            return None
        return self.capacity - len(self.enrolled_students)
    
    def enroll_student(self, student_id: str) -> bool:
        """
        学生选课
        
        Args:
            student_id (str): 学生学号
            
        Returns:
            bool: 选课成功返回True，否则返回False
        """
        if student_id in self.enrolled_students:
            print(f"错误：学生 {student_id} 已选修该课程")
            return False
        
        if self.is_full():
            print(f"错误：课程已满，无法选课")
            return False
        
        if self.status != CourseStatus.OPEN:
            print(f"错误：课程当前状态为 {self.status.value}，无法选课")
            return False
        
        self.enrolled_students.add(student_id)
        print(f"学生 {student_id} 选课成功")
        return True
    
    def drop_student(self, student_id: str) -> bool:
        """
        学生退课
        
        Args:
            student_id (str): 学生学号
            
        Returns:
            bool: 退课成功返回True，否则返回False
        """
        if student_id not in self.enrolled_students:
            print(f"错误：学生 {student_id} 未选修该课程")
            return False
        
        self.enrolled_students.remove(student_id)
        print(f"学生 {student_id} 退课成功")
        return True
    
    def is_student_enrolled(self, student_id: str) -> bool:
        """
        检查学生是否已选课
        
        Args:
            student_id (str): 学生学号
            
        Returns:
            bool: 已选课返回True，否则返回False
        """
        return student_id in self.enrolled_students
    
    def get_enrolled_students(self) -> List[str]:
        """
        获取已选课学生列表
        
        Returns:
            List[str]: 学生学号列表
        """
        return list(self.enrolled_students)
    
    def get_enrollment_count(self) -> int:
        """
        获取选课人数
        
        Returns:
            int: 选课人数
        """
        return len(self.enrolled_students)
    
    def get_enrollment_rate(self) -> Optional[float]:
        """
        获取选课率
        
        Returns:
            Optional[float]: 选课率（百分比），容量不限时返回None
        """
        if self.capacity == 0:
            return None
        return (len(self.enrolled_students) / self.capacity) * 100
    
    def get_course_info(self) -> str:
        """
        获取课程详细信息的格式化字符串
        
        Returns:
            str: 格式化的课程信息
        """
        info = f"""
=== 课程信息 ===
课程名称: {self.name}
课程代码: {self.course_code}
课程类型: {self.course_type.value}
课程状态: {self.status.value}
学分: {self.credits}
学时: {self.hours}
"""
        
        if self.semester:
            info += f"开课学期: {self.semester}\n"
        
        if self.teacher_id:
            info += f"授课教师: {self.teacher_id}\n"
        
        if self.classroom:
            info += f"上课教室: {self.classroom}\n"
        
        if self.schedule:
            info += f"\n=== 上课时间 ===\n"
            for item in self.schedule:
                info += f"  {item['weekday']} {item['start_time']}-{item['end_time']}\n"
        
        if self.prerequisites:
            info += f"\n先修课程: {', '.join(self.prerequisites)}\n"
        
        if self.description:
            info += f"\n课程描述: {self.description}\n"
        
        info += f"\n=== 选课统计 ===\n"
        info += f"已选人数: {self.get_enrollment_count()}\n"
        
        if self.capacity > 0:
            info += f"课程容量: {self.capacity}\n"
            info += f"剩余名额: {self.get_available_seats()}\n"
            enrollment_rate = self.get_enrollment_rate()
            if enrollment_rate is not None:
                info += f"选课率: {enrollment_rate:.1f}%\n"
        else:
            info += f"课程容量: 不限\n"
        
        return info
    
    def __str__(self) -> str:
        """字符串表示"""
        return f"Course(name='{self.name}', code='{self.course_code}', enrolled={len(self.enrolled_students)})"
    
    def __repr__(self) -> str:
        """对象表示"""
        return self.__str__()


def demonstrate_course_management():
    """演示课程管理功能"""
    print("=== 课程管理系统演示 ===\n")
    
    # 创建课程对象
    course1 = Course("数据结构", "CS201", 4.0, 64)
    course1.set_capacity(50)
    course1.set_teacher("T2021001")
    course1.set_course_type(CourseType.REQUIRED)
    course1.set_semester("2025-春季")
    course1.set_classroom("教学楼A201")
    course1.set_description("本课程介绍常用数据结构的原理、算法及应用")
    course1.add_schedule("周一", "08:00", "09:40")
    course1.add_schedule("周三", "10:00", "11:40")
    course1.set_status(CourseStatus.OPEN)
    
    course2 = Course("算法设计与分析", "CS301", 3.0, 48)
    course2.set_capacity(40)
    course2.set_teacher("T2021001")
    course2.set_course_type(CourseType.PROFESSIONAL)
    course2.add_prerequisite("CS201")
    course2.set_semester("2025-秋季")
    course2.set_status(CourseStatus.PLANNING)
    
    # 学生选课
    print("1. 学生选课:")
    course1.enroll_student("2021001")
    course1.enroll_student("2021002")
    course1.enroll_student("2021003")
    course1.enroll_student("2021004")
    course1.enroll_student("2021005")
    
    # 显示课程信息
    print("\n2. 显示课程信息:")
    print(course1.get_course_info())
    print(course2.get_course_info())
    
    # 查询选课情况
    print("\n3. 查询选课情况:")
    print(f"数据结构已选人数: {course1.get_enrollment_count()}")
    print(f"数据结构剩余名额: {course1.get_available_seats()}")
    print(f"数据结构选课率: {course1.get_enrollment_rate():.1f}%")
    
    # 学生退课
    print("\n4. 学生退课:")
    course1.drop_student("2021003")
    print(f"退课后剩余名额: {course1.get_available_seats()}")


if __name__ == "__main__":
    demonstrate_course_management()
