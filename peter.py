import sys
from ai_master import Master
from task_manager import TaskManager
from tasks import *
from teacher_tasks import TeacherTask
from prompt_factory import PromptFactory
from models.model_factory import ModelFactory
from id_generator import PersistentIDGenerator

class Assistant:
    def __init__(self, name):
        self.name = name
        self.task_manager = TaskManager()
        self._model = ModelFactory.get_model_class("GPT4")
        self.user2taskid = {} #uid to taskid list
    
    def add_task(self, task_type, **args): 
        _id = PersistentIDGenerator.generate_id()#course_id and task_id
        if task_type == REMINDERTASK:
            t = ReminderTaskRepeat(args["name"], args["period"], args["content"])
        elif task_type == JOKETASK:
            t = JokeTask(args["name"], args["joke_type"])
        elif task_type == TEACHERTASK:
            uid = args["uid"]
            t = TeacherTask(args["title"], _id, uid)
            self.task_manager.id2task[_id] = t
            if uid not in self.user2taskid: 
                self.user2taskid[uid] = []
            self.user2taskid[uid].append(_id)
        self.task_manager.add_task(t)
        return _id

    def serve(self):
        self.greet()
        while True:
            self.check_goal()
            self.impl_tasks()

            time.sleep(3)

        return

    def answer(self, data):
        """
        重要的入口函数
        做需求分析
        """
        try:
            #message = data['text'] #get structed data by model api
            message = data
            req_str = PromptFactory.get_title_prompt(message)
            parse_res = self._model.request(req_str)
            if len(parse_res) and parse_res != "No":
                title_to_confirm = parse_res
            else:
                return False, "can't understand study topic"

            #self.add_task(TEACHERTASK, title)
        except Exception as e:
            #logger
            return False, str(e)

        return True, title_to_confirm

    def check_goal(self):
        return

    def impl_tasks(self):
        self.task_manager.check_and_run()
        return

    def greet(self):
        print(f"Hello, my name is {self.name}")


    # 静态方法
    @staticmethod
    def static_method_example():
        print("This is a static method.")

    @classmethod
    def create_with_default_name(cls):
        return cls("Default") 


if __name__ == "__main__":
    master1 = Master("Jack", 30)
    perter1 = Assistant("Alice")

    perter1.greet() #
    perter1.add_task(REMINDERTASK, name="test_task1", period=2, content = "drink water")
    perter1.add_task(JOKETASK, name="daily_joke", joke_type="sex")
    perter1.add_task(TEACHERTASK, name="study_1")
    perter1.serve()

