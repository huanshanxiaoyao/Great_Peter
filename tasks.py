import time
from models.model_factory import ModelFactory

REMINDERTASK = 1
JOKETASK = 2
TEACHERTASK = 3

class Task():
    """"""
    def __init__(self, name):
        self.name = name
    
    def check(self):
        return

class JokeTask(Task):
    def __init__(self, name, joke_type):
        super().__init__(name)
        self.type = joke_type
        self.joke_model = ModelFactory.get_model_class("DeepSeek")
        self.trigger_timings = []

    def check(self):
        #TODO
        if len(self.trigger_timings) > 2 and self.trigger_timings[-1] +180 > time.time():
            print("skip once")
            return


        req_content = "Tell me a funny story on %s"%self.type
        message = self.joke_model.request(req_content)
        print("This is a joke (type:%s), %s"%(self.type, message))
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
