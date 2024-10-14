import json
from log_config import main_logger

class HomeWork():
    def __init__(self, rel_chapter_title):
        self.title = rel_chapter_title
        self.open_questions = []
        self.closed_questions = []

class Chapter():
    def __init__(self, title, content, ref):
        self.title = title
        self.content = content
        self.ref = ref
        self.status = 0
        self.eval_score = []

class InterestCourse():
    """
    AI辅导的 兴趣课程，有如下特点
    1, 学习内容由学生主动选择 ，然后与导师确认
    2, 分课时制定教学提纲，但学习时间灵活，导师适当提醒
    3, 每节课导师输出教案，学生可通过对话方式提出问题讨论
    4, 学生根据参考文献做进一步学习，然后完成每课时作业
    5, 导师出考核内容，并自主判卷，如担心准确性，可引入其他导师(Agent)校验
    """
    def __init__(self, name):
        self.name = name
        self.chapters = []


    def set_plan(self, outline_content):
        """
        outline_content got from AI
        因为 AI 返回内容格式并不完全可控，因此需要做较多检查
        """
        
        error_str = None
        data = []
        try:
            data = json.loads(outline_content)
        except json.JSONDecodeError as e:
            error_str = "JSONDecodeError:%s"%e
            main_logger.error(error_str)
        except TypeError as e:
            error_str = "TypeError:%s"%e
            main_logger.error(error_str)
        except Exception as e:
            error_str = "Other Error:%s"%e
            main_logger.error(error_str)

        if error_str:
            return False, error_str

        if "chapters" not in data:
            main_logger.error("no weeks key in data")
            return False, "key errro in data"
        chapters = data["chapters"]
        self.class_hour = len(chapters)
        for chap in chapters:
            title = chap['title']
            content = chap['content']
            ref = chap['ref']
            self.chapters.append(Chapter(title, content, ref))

        main_logger.info("Success load data and build plan")
        return True, error_str

    
    def pick_chapter(self, idx=-1):
        """
        if idx gived return idx th chapter, otherwise return next un-finished chapter
        """
        if idx > -1 and idx < len(self.chapters):
            return idx, self.chapters[idx]
        for idx, chap in enumerate(self.chapters):
            if chap.status == 0:
                return idx, chap


    def study_hour(self):
        """
        完成一个课时的学习
        """

        chap_idx, slected_chapter = self.pick_chapter()

        #step1, 构造 prompt, 查询AI 得到提纲
        prompt = get_chapter_outline(self.title, slected_chapter.title, slected_chapter.content, slected_chapter.ref)
        

    def update_progress(self):
        return
