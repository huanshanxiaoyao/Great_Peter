import json
from tasks import Task
from models.model_factory import ModelFactory

class TeacherTask():
    def __init__(self, name):
        super().__init__()


        #
        self.course_name = ""
        self.course_requirement = ""
        self.teacher_model = ModelFactory.get_model_class("DeepSeek")

    def check(self):
        self.requirement_set()
        return


    def requirement_set(self):
        course_title = "法国历史"
        study_chapters = 10
        outline_prompt = "现在有一个比较重要且有难度的工作，你作为一个指导老师，帮助一个大学生自学%s，\
                使他可以在未来%d 节课，每节花1 个小时左右，对%s的认知提升一个大的台阶，\
                首先 我们要有一个学习提纲，包含学习的目录，以及每一部分要参考的文献；你还要负责细化拆解后面课程，\
                提升学生的学习兴趣和效果，包括最终的考核，好了 现在你来想想如何推进这个工作, 然后输出教学大纲,\
                采用 json 格式, 第一级 key:chapters: 对应一个数组包含每周的学习内容，其中必须有的字段title:本章标题,  content:学习内容，ref:参考文献" \
                %(course_title, study_chapters, course_title)
        req_content = outline_prompt
        message = self.teacher_model.request(req_content)
        print(message)
        return

if __name__ == "__main__":
    task1 = TeacherTask("taks1")
    task1.check()
