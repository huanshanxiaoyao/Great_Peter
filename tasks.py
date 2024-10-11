import time

class Task():
    """"""
    def __init__(self, name):
        self.name = name
    
    def check(self):
        return

class JokeTask():
    def __init__(self, name, joke_type):
        super().__init__()
        self.type = joke_type

    def check(self):
        print("This is a joke (type:%s)"%self.type)
        return


class ReminderTask(Task):
    """"""
    def __init__(self, name, text):
        super().__init__(name)
        self.content = text

    def remind(self):
        print("Hello, %s"%self.content)
        return

class ReminderTaskOnce(ReminderTask):
    """"""
    def __init__(self, name, text, trigger_time):
        super().__init__(name, text)
        self.trigger_time = trigger_time

    def check(self):
        distance = trigger_time - time.time()
        if distance < 1:
            self.remind()
        return distance

class ReminderTaskRepeat(ReminderTask):
    """"""
    def __init__(self, name, period, text):
        super().__init__(name, text)
        period = int(period)
        self.period = period # 暂定小时为单位
        self.next_time = time.time() + period * 6
        #self.next_time = time.now() + period * 3600

    def check(self):
        distance = self.next_time - time.time()
        if distance < 1:
            self.remind()
            self.next_time += self.period
