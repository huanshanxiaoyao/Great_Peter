
class TaskManager:
    def __init__(self):
        self.taskList = []

    def add_task(self, t):
        self.taskList.append(t)

    def check_and_run(self):
        for t in self.taskList:
            t.check()
