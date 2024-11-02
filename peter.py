import sys
import os
import json
import time
from log_config import logger
from ai_master import Master
from task_manager import TaskManager
from tasks import *
from teacher_tasks import TeacherTask
from prompt_factory import PromptFactory
from models.model_factory import ModelFactory
from id_generator import PersistentIDGenerator

class Assistant:
    """
    一个 Assistant 对应一个用户，还是多个？
    目前是对应多个
    """
    def __init__(self, name):
        self.name = name
        self.task_manager = TaskManager()
        self._model = ModelFactory.get_model_class("GPT4")
        self.user2taskid = {} #uid to taskid list

        self.storage_file = "pdata/peter_storage.json"
        self._load_from_storage()
    
    def add_task(self, task_type, **args): 

        task_id = PersistentIDGenerator.generate_task_id() #course_id and task_id

        if task_type == REMINDERTASK:
            t = ReminderTaskRepeat(args["name"], args["period"], args["content"])
        elif task_type == JOKETASK:
            t = JokeTask(args["name"], args["joke_type"])
        elif task_type == TEACHERTASK:
            if not ("uid" in args and "title" in args):
                logger.error("no uid or title for create a TeacherTask")
                return -1

            uid = args["uid"]
            t = TeacherTask(args["title"], task_id, args["uid"])
            if uid not in self.user2taskid: 
                self.user2taskid[uid] = []
            self.user2taskid[uid].append(task_id)
        self.task_manager.add_task(t)
        return task_id

    def serve(self):
        self.greet()
        while True:
            self.check_goal()
            self.impl_tasks()
            self._save_to_storage()
            time.sleep(3)

        return

    def answer(self, data):
        """
        重要的入口函数
        做需求分析
        目前只解析是否学习某类知识
        """
        try:
            message = data
            req_str = PromptFactory.get_title_prompt(message)
            parse_res = self._model.request(req_str)
            if len(parse_res) and parse_res != "No":
                title_to_confirm = parse_res
            else:
                logger.error("can't understand study topic")
                return False, "can't understand study topic"

        except Exception as e:
            logger.error(str(e))
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
    
    def _save_to_storage(self):
        id2taskinfo = {t.id: t.to_dict() for t in self.task_manager.id2task.values()}
        data = {"user2taskid": self.user2taskid, "id2taskinfo": id2taskinfo}
        with open(self.storage_file, "w") as f:
            json.dump(data, f, ensure_ascii=False)

    def _load_from_storage(self):
        if os.path.exists(self.storage_file):
            with open(self.storage_file, "r") as f:
                data = json.load(f)
                for k, v in data["user2taskid"].items():
                    self.user2taskid[int(k)] = v

                print("user2taskid:%s"%str(self.user2taskid))

                id2taskinfo = data["id2taskinfo"]
                for t in id2taskinfo.values():
                    task = TeacherTask.from_dict(t)
                    self.task_manager.add_task(task)
        else:
            logger.error("storage file not found")


if __name__ == "__main__":
    master1 = Master("Jack", 30)
    perter1 = Assistant("Alice")

    perter1.greet() #
    perter1.add_task(REMINDERTASK, name="test_task1", period=2, content = "drink water")
    perter1.add_task(JOKETASK, name="daily_joke", joke_type="sex")
    perter1.add_task(TEACHERTASK, name="study_1")
    perter1.serve()

