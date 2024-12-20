import os
import json
from log_config import logger

class HomeWork():
    def __init__(self, rel_chapter_title):
        self.title = rel_chapter_title
        self.open_questions = []
        self.closed_questions = []

class Chapter():
    def __init__(self, title, content, ref, status=0, detail_content=""):
        self.title = title
        self.content = content
        self.ref = ref
        self.status = status
        self.detail_content = detail_content

    def to_dict(self):
        return {
            "title": self.title,
            "content": self.content,
            "ref": self.ref,
            "status": self.status,
            "detail_content": self.detail_content
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(data["title"], data["content"], data["ref"], data["status"], data["detail_content"])

class Course():
    """
    AI辅导的 兴趣课程，有如下特点
    1, 学习内容由学生主动选择 ，然后与导师确认
    2, 分课时制定教学提纲，但学习时间灵活，导师适当提醒
    3, 每节课导师输出教案，学生可通过对话方式提出问题讨论
    4, 学生根据参考文献做进一步学习，然后完成每课时作业
    5, 导师出考核内容，并自主判卷，如担心准确性，可引入其他导师(Agent)校验
    """
    def __init__(self, cid, name):
        self.id = cid
        self.name = name
        self.chapters = []
        self.storage_file = "pdata/course_storage_%s.json"%cid

        self._load_from_storage()

    def format_chapter_outline(self, outline_content):
        data, error_str = self.try_load_json(outline_content) 
        if len(data) == 0:
            logger.error("data == 0")
            return False, error_str


        if "topics" not in data:
            logger.error("no topics key in data")
            return False, "key errro in data"
        topics = data["topics"]
        return True, topics

    def check_next_chapter(self):
        """返回下一个未学习的 chapter 的 idx"""
        idx = -1
        for i, chap in enumerate(self.chapters):
            if chap.status == 0:
                idx = i
                break
        return idx
            

    def set_plan(self, outline_content):
        """
        outline_content got from AI
        因为 AI 返回内容格式并不完全可控，因此需要做较多检查
        """
        data, error_str = self.try_load_json(outline_content) 
        if len(data) == 0:
            return False, error_str


        if "chapters" not in data:
            logger.error("no weeks key in data")
            return False, "key errro in data"
        chapters = data["chapters"]
        self.class_hour = len(chapters)
        for chap in chapters:
            title = chap['title']
            content = chap['content']
            ref = chap['ref']
            self.chapters.append(Chapter(title, content, ref))
            self._save_to_storage()

        logger.info("Success load data and build plan")
        return True, error_str

    def show_outlines(self): 
        show_info = {}
        for i in range(len(self.chapters)):
            show_info[i] = [self.chapters[i].title, self.chapters[i].content]
        show_str = json.dumps(show_info, ensure_ascii=False)
        #print(show_str)
        return show_str

    def try_load_json(self, content):
        error_str = None
        data = []
        try:
            data = json.loads(content)
        except json.JSONDecodeError as e:
            error_str = "JSONDecodeError:%s"%e
            logger.error(error_str + "json_str:" + content)
        except TypeError as e:
            error_str = "TypeError:%s"%e
            logger.error(error_str)
        except Exception as e:
            error_str = "Other Error:%s"%e
            logger.error(error_str)

        if error_str:
            return [], error_str

        return data, "Done"

    def _save_to_storage(self):

        data = {"chapters":[chap.to_dict() for chap in self.chapters] }

        with open(self.storage_file, "w") as file:
            json.dump(data, file, ensure_ascii=False)

    def _load_from_storage(self):
        if os.path.exists(self.storage_file):
            with open(self.storage_file, "r") as file:
                data = json.load(file)
                self.chapters = [Chapter.from_dict(chap) for chap in data.get("chapters", [])]
        else:
            self.chapters = []

   
