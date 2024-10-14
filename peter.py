import sys
from ai_master import Master
from task_manager import TaskManager
from tasks import *
from teacher_tasks import TeacherTask

class Assistant:
    def __init__(self, name, master):
        self.name = name
        self.master = master
        self.task_manager = TaskManager()
    
    def add_task(self, task_type, **args): 
        if task_type == REMINDERTASK:
            t = ReminderTaskRepeat(args["name"], args["period"], args["content"])
        elif task_type == JOKETASK:
            t = JokeTask(args["name"], args["joke_type"])
        elif task_type == TEACHERTASK:
            t = TeacherTask(args["name"])
        self.task_manager.add_task(t)
        return 

    def serve(self):
        self.greet()
        while True:
            self.check_new_request()
            self.check_goal()
            self.impl_tasks()

            time.sleep(3)

        return

    def check_new_request(self):
        return

    def check_goal(self):
        return

    def impl_tasks(self):
        self.task_manager.check_and_run()
        return

    def greet(self):
        print(f"Hello, my name is {self.name} and my master is {self.master.name}")


    # 静态方法
    @staticmethod
    def static_method_example():
        print("This is a static method.")

    # 类方法
    @classmethod
    def create_with_default_name(cls, master):

        return cls("Default", master) 


if __name__ == "__main__":
    master1 = Master("Jack", 30)
    perter1 = Assistant("Alice", master1)

    perter1.greet() #
    perter1.add_task(REMINDERTASK, name="test_task1", period=2, content = "drink water")
    perter1.add_task(JOKETASK, name="daily_joke", joke_type="sex")
    perter1.add_task(TEACHERTASK, name="study_1")
    perter1.serve()


    # 使用静态方法
    #Assistant.static_method_example()  #

    # 使用类方法创建实例
    #master2 = Master("Bob")
    #person2 = Assistant.create_with_default_name(master2)
    #person2.greet() 

