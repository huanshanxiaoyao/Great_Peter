import json
from tasks import Task
from models.model_factory import ModelFactory
from course import InterestCourse

class TeacherTask():
    def __init__(self, name):
        super().__init__()
        #
        self.course_name = ""
        self.course_requirement = ""
        self.teacher_model = ModelFactory.get_model_class("DeepSeek")
    

    def check(self):
        print("Check Task:%s"%self.course_name)
        
        """
        success, interest_course =  self.set_requirement():
        if not success:
            #logger
            return False

        #TODO

        #self.study_hour(course)
        return
        """

    def study_hour(self, course):
        """
        完成一个课时的学习
        """

        chap_idx, slected_chapter = self.pick_chapter(course)

        #step1, 构造 prompt, 查询AI 得到提纲
        prompt = get_chapter_outline(self.title, slected_chapter.title, slected_chapter.content, slected_chapter.ref)

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

    def set_requirement(self, course_title, study_chapters):
        course_title = "法国历史"
        study_chapters = 10
        outline_prompt = PromptFactory.get_course_outline_prompt(course_title, study_chapters, course_title)
        print(outline_prompt)
        message = self.teacher_model.request(outline_prompt)
        course = InterestCourse(course_title)

        try_count = 1
        success = False

        while try_count < 3:
            print(message)
            ret, _err = course.set_plan(message)
            if ret:
                success = True
                break
            new_prompt = "请按照要求输出下面问题答复" + outline_prompt
            message = self.teacher_model.request(new_prompt)
            try_count += 1

        return success, course

if __name__ == "__main__":
    task1 = TeacherTask("taks1")
    task1.check()
