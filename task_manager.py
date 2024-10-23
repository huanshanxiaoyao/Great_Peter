import time
import threading

class TaskManager:
    def __init__(self):
        self.id2task = {}

        self.lock = threading.Lock()

        #taskMessages 目前的设计是配合客户端的轮询通信
        self.taskMessages = {}

    def add_task(self, task):
        self.id2task[task.id] = task

    def check_and_run(self):
        for t in self.id2task.values():
            ret, message_dict = t.check()
            #TODO 不是特别好的实现方式
            if not ret:
                continue
            with self.lock:
                self.taskMessages[t.uid] = message_dict
        time.sleep(3) #TODO
