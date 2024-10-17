import json
from tasks import Task
from models.model_factory import ModelFactory
from course import Course
from prompt_factory import PromptFactory

class TeacherTask(Task):
    """
    10.16 再更正下 TeacherTask的定义
    每个实力，对应一个用户的一个学习课程
    和 Course 类的区割: TeacherTask 重点关注业务流程，老师视角，动态；
    Course类 尽量是只关于课程教案，作业等 paperwork，静态视角
    """
    def __init__(self, course_name, _id, uid):
        super().__init__(course_name, _id, uid)
        #
        self.course_name = course_name
        self.course = None
        self.teacher_model = ModelFactory.get_model_class("GPT4")

        # 当前课程状态
        # 0 为开题, 1 学习中, 2 章节学完，未考核, 3 完成学习和考核
        self.status = 0
    

    def check(self):
        print("Check Task:%s"%self.course_name)

        success = False
        #根据执行情况  产出要添加的触发消息
        task_message = {}

        if self.status == 0:
            success, course =  self.set_requirement(self.course_name)
            if not success:
                #TODO logging
                return False, task_message
            self.course = course
            self.status = 1

            task_message = {"info":"course %s ready, you can start", \
                    "course_title":self.course_name,\
                    "course_id":self.id,\
                    "outline_content":self.course.show_outlines(),\
                    "next_idx": 0}

        elif self.status == 1:
            success = self.study_hour(self.course)
            if not success:
                #TODO logging
                return False, task_message
            #
            idx = self.course.check_next_chapter()
            if idx > -1:
                task_message = {"info":"you can start next chapter", \
                        "course_title": self.course_name,\
                        "course_id":self.id,\
                        "next_idx":idx}
                pass
            else:
                self.status = 2
                task_message = {"info":"Great!,you finish all chapters", \
                        "course_title": self.course_name,\
                        "course_id":self.id,\
                        "next_idx":-1}
        else:
            #TODO 先跳过，后面再实现
            pass
        return success, task_message
        

    def study_hour(self, course):
        """
        完成一个课时的学习
        """
        if not course:
            #TODO
            return 

        chap_idx, slected_chapter = self.pick_chapter(course)

        #step1, 构造 prompt, 查询AI 得到提纲
        prompt = PromptFactory.get_chapter_outline_prompt(self.course_name, slected_chapter.title, slected_chapter.content, slected_chapter.ref)

        message = self.teacher_model.request(prompt)

        try_count = 1

        while try_count < 3:
            #尝试解析
            ret, erro_info = course.format_chapter_outline(message)
            new_prompt = "请按要求重新回答:" + prompt
            message = self.teacher_model.request(new_prompt)

        #step2, 
        return 
        

    def update_progress(self):
        return


    def pick_chapter(self, course, idx=-1):
        """
        if idx gived return idx th chapter, otherwise return next un-finished chapter
        """
        if idx > -1 and idx < len(course.chapters):
            return idx, course.chapters[idx]
        for idx, chap in enumerate(course.chapters):
            if chap.status == 0:
                return idx, chap

    def set_requirement(self, course_title, study_chapters=10):
        outline_prompt = PromptFactory.get_course_outline_prompt(self.course_name, study_chapters)
        print(outline_prompt)
        message = self.teacher_model.request(outline_prompt)
        print(message)
        ###TODO
        message = message[message.find('{'):message.rfind('}')+1]
        print(message)
        course = Course(course_title)

        try_count = 1
        success = False

        while try_count < 3:
            ret, _err = course.set_plan(message)
            if ret:
                success = True
                break
            new_prompt = "请按照要求输出下面问题答复" + outline_prompt
            message = self.teacher_model.request(new_prompt)
            message = message[message.find('{'):message.rfind('}')+1]
            print(message)
            try_count += 1

        return success, course

if __name__ == "__main__":
    task1 = TeacherTask("法国历史")
    task1.check()
