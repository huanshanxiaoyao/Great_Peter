import time
import threading

class TaskManager:
    def __init__(self):
        self.taskList = []

        self.lock = threading.Lock()
        self.taskMessages = {}

    def add_task(self, t):
        self.taskList.append(t)

    def check_and_run(self):
        for t in self.taskList:
            ret, message_dict = t.check()
            #TODO 不是特别好的实现方式
            if not ret:
                continue
            with self.lock:
                self.taskMessages[t.uid] = message_dict
        time.sleep(3) #TODO
