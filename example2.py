# 始终生效

class Student:
    """
    学生类
    """
    def __init__(self, name, age, grade):
        self.name = name
        self.age = age
        self.grade = grade
    
    def introduce(self):
        """
        自我介绍
        """
        return f"我叫{self.name}，今年{self.age}岁，在{self.grade}年级。"
    
    def study(self, subject):
        """
        学习方法
        """
        return f"{self.name}正在学习{subject}。"


def main():
    student = Student("小明", 15, "高一")
    print(student.introduce())
    print(student.study("数学"))


if __name__ == "__main__":
    main()
