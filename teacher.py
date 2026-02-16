#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
文件名: teacher.py
作者: 开发者
创建日期: 2025-10-11
版本: 1.0
描述: 教师信息管理的Python类文件
      包含教师的基本信息管理和课程管理功能
功能:
  - 教师基本信息管理（姓名、年龄、工号、部门）
  - 授课课程管理
  - 教师统计信息
依赖: 无外部依赖，仅使用Python标准库
使用示例:
  teacher = Teacher("王老师", 35, "T2021001", "计算机学院")
  teacher.add_course("数据结构")
  teacher.add_course("算法设计")
  print(teacher.get_teacher_info())
修改记录:
  2025-10-11 - 初始版本创建
"""

from typing import List, Dict, Optional
from datetime import datetime


class Teacher:
    """教师类 - 管理教师的基本信息和授课信息"""
    
    def __init__(self, name: str, age: int, teacher_id: str, department: str = ""):
        """
        初始化教师对象
        
        Args:
            name (str): 教师姓名
            age (int): 教师年龄
            teacher_id (str): 工号
            department (str): 所属部门/学院，默认为空字符串
        """
        self.name = name
        self.age = age
        self.teacher_id = teacher_id
        self.department = department
        self.courses: List[str] = []  # 授课课程列表
        self.students: Dict[str, List[str]] = {}  # 课程对应的学生列表
        self.created_time = datetime.now()
        self.title = "讲师"  # 职称
        self.email = ""
        self.phone = ""
    
    def add_course(self, course_name: str) -> bool:
        """
        添加授课课程
        
        Args:
            course_name (str): 课程名称
            
        Returns:
            bool: 添加成功返回True，课程已存在返回False
        """
        if course_name in self.courses:
            print(f"警告：课程 '{course_name}' 已存在于授课列表中")
            return False
        
        self.courses.append(course_name)
        self.students[course_name] = []
        print(f"成功添加课程: {course_name}")
        return True
    
    def remove_course(self, course_name: str) -> bool:
        """
        移除授课课程
        
        Args:
            course_name (str): 课程名称
            
        Returns:
            bool: 删除成功返回True，课程不存在返回False
        """
        if course_name not in self.courses:
            print(f"错误：课程 '{course_name}' 不在授课列表中")
            return False
        
        self.courses.remove(course_name)
        if course_name in self.students:
            del self.students[course_name]
        print(f"成功移除课程: {course_name}")
        return True
    
    def add_student_to_course(self, course_name: str, student_id: str) -> bool:
        """
        将学生添加到指定课程
        
        Args:
            course_name (str): 课程名称
            student_id (str): 学生学号
            
        Returns:
            bool: 添加成功返回True，否则返回False
        """
        if course_name not in self.courses:
            print(f"错误：课程 '{course_name}' 不在授课列表中")
            return False
        
        if student_id in self.students[course_name]:
            print(f"警告：学生 {student_id} 已在课程 '{course_name}' 中")
            return False
        
        self.students[course_name].append(student_id)
        print(f"成功将学生 {student_id} 添加到课程 '{course_name}'")
        return True
    
    def remove_student_from_course(self, course_name: str, student_id: str) -> bool:
        """
        将学生从指定课程中移除
        
        Args:
            course_name (str): 课程名称
            student_id (str): 学生学号
            
        Returns:
            bool: 移除成功返回True，否则返回False
        """
        if course_name not in self.courses:
            print(f"错误：课程 '{course_name}' 不在授课列表中")
            return False
        
        if student_id not in self.students[course_name]:
            print(f"错误：学生 {student_id} 不在课程 '{course_name}' 中")
            return False
        
        self.students[course_name].remove(student_id)
        print(f"成功将学生 {student_id} 从课程 '{course_name}' 中移除")
        return True
    
    def get_courses(self) -> List[str]:
        """
        获取所有授课课程
        
        Returns:
            List[str]: 课程列表
        """
        return self.courses.copy()
    
    def get_students_by_course(self, course_name: str) -> Optional[List[str]]:
        """
        获取指定课程的学生列表
        
        Args:
            course_name (str): 课程名称
            
        Returns:
            Optional[List[str]]: 学生列表，课程不存在返回None
        """
        if course_name not in self.courses:
            return None
        return self.students[course_name].copy()
    
    def get_total_students(self) -> int:
        """
        获取所有课程的学生总数（去重）
        
        Returns:
            int: 学生总数
        """
        all_students = set()
        for students in self.students.values():
            all_students.update(students)
        return len(all_students)
    
    def get_workload(self) -> Dict[str, int]:
        """
        获取工作量统计
        
        Returns:
            Dict[str, int]: 包含课程数和学生数的字典
        """
        return {
            "course_count": len(self.courses),
            "total_students": self.get_total_students(),
            "avg_students_per_course": self.get_total_students() / len(self.courses) if self.courses else 0
        }
    
    def set_title(self, title: str) -> None:
        """
        设置职称
        
        Args:
            title (str): 职称（如：助教、讲师、副教授、教授）
        """
        self.title = title
        print(f"职称已更新为: {title}")
    
    def set_contact_info(self, email: str = None, phone: str = None) -> None:
        """
        设置联系方式
        
        Args:
            email (str): 电子邮箱
            phone (str): 电话号码
        """
        if email:
            self.email = email
        if phone:
            self.phone = phone
        print("联系方式已更新")
    
    def get_teacher_info(self) -> str:
        """
        获取教师详细信息的格式化字符串
        
        Returns:
            str: 格式化的教师信息
        """
        info = f"""
=== 教师信息 ===
姓名: {self.name}
职称: {self.title}
年龄: {self.age}
工号: {self.teacher_id}
部门: {self.department}
入职时间: {self.created_time.strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        if self.email:
            info += f"邮箱: {self.email}\n"
        if self.phone:
            info += f"电话: {self.phone}\n"
        
        info += f"\n=== 授课信息 ===\n"
        
        if not self.courses:
            info += "暂无授课课程\n"
        else:
            info += f"授课课程数: {len(self.courses)}\n"
            for course in self.courses:
                student_count = len(self.students.get(course, []))
                info += f"  - {course} ({student_count} 名学生)\n"
            
            workload = self.get_workload()
            info += f"\n=== 工作量统计 ===\n"
            info += f"课程总数: {workload['course_count']}\n"
            info += f"学生总数: {workload['total_students']}\n"
            info += f"平均每门课程学生数: {workload['avg_students_per_course']:.1f}\n"
        
        return info
    
    def __str__(self) -> str:
        """字符串表示"""
        return f"Teacher(name='{self.name}', teacher_id='{self.teacher_id}', courses={len(self.courses)})"
    
    def __repr__(self) -> str:
        """对象表示"""
        return self.__str__()


def demonstrate_teacher_management():
    """演示教师管理功能"""
    print("=== 教师管理系统演示 ===\n")
    
    # 创建教师对象
    teacher1 = Teacher("王老师", 35, "T2021001", "计算机学院")
    teacher1.set_title("副教授")
    teacher1.set_contact_info(email="wang@university.edu.cn", phone="13800138000")
    
    teacher2 = Teacher("李老师", 42, "T2019005", "数学学院")
    teacher2.set_title("教授")
    
    # 添加课程
    print("1. 添加授课课程:")
    teacher1.add_course("数据结构")
    teacher1.add_course("算法设计")
    teacher1.add_course("操作系统")
    
    teacher2.add_course("高等数学")
    teacher2.add_course("线性代数")
    
    # 添加学生
    print("\n2. 添加学生到课程:")
    teacher1.add_student_to_course("数据结构", "2021001")
    teacher1.add_student_to_course("数据结构", "2021002")
    teacher1.add_student_to_course("数据结构", "2021003")
    teacher1.add_student_to_course("算法设计", "2021001")
    teacher1.add_student_to_course("算法设计", "2021004")
    
    # 显示教师信息
    print("\n3. 显示教师信息:")
    print(teacher1.get_teacher_info())
    print(teacher2.get_teacher_info())
    
    # 查询特定课程的学生
    print("\n4. 查询课程学生:")
    students = teacher1.get_students_by_course("数据结构")
    print(f"数据结构课程学生: {students}")


if __name__ == "__main__":
    demonstrate_teacher_management()
