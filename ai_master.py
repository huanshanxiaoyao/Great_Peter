import sys

class Master:
    def __init__(self, name, age=0):
        self.name = name  # 实例属性
        self.age = age

    def get_name(self):
        return self.name

    # 实例方法
    def greet(self):
        print(f"Hello, my name is {self.name} and I am {self.age} years old.")


    # 静态方法
    @staticmethod
    def static_method_example():
        print("This is a static method.")

    # 类方法
    @classmethod
    def create_with_default_age(cls, name):
        return cls(name, 30)  # 创建一个新对象，默认年龄为 30


if __name__ == "__main__":
    # 创建一个实例
    person1 = Master("Alice", 25)

    # 调用类的方法
    person1.greet()  # 输出: Hello, my name is Alice and I am 25 years old.


    # 使用静态方法
    Master.static_method_example()  # 输出: This is a static method.

    # 使用类方法创建实例
    person2 = Master.create_with_default_age("Bob")
    person2.greet()  # 输出: Hello, my name is Bob and I am 30 years old.

