

class PromptFactory:
    @staticmethod
    def get_chapter_outline_prompt(course_title, chapter_title, chapter_content, chapter_ref):
        outline_prompt = f"我们正在学习 %{course_title}, 今天的章节是%{chapter_title}, \
                主要内容有 %{chapter_content}, 参考文献:%{chapter_ref}, 请认真思考给出本节的教学提纲,\
                建议分3-8个 topic（可视内容多少调整）, 其中每个 topic 包含 title(20字以内) 和 content(200字左右）两部分,\
                返回内容严格采用 json 格式, 第一级目录key:topics,为一个数组，其中每个元素有 title和 content 两个字段"
        return outline_prompt


if __name__ == "__main__":
    from models.model_factory import ModelFactory
    test_model = ModelFactory.get_model_class("GPT4")
    course_title = "法国历史"
    chapter_title = "中世纪的法国"
    chapter_content = " 法兰克王国的兴起,  加洛林王朝与查理大帝,  封建制度的形成"
    chapter_ref = "《中世纪的结构》, 《查理大帝传》"

    req_content = PromptFactory.get_chapter_outline_prompt(course_title, chapter_title, chapter_content, chapter_ref)
    message = test_model.request(req_content)
    print(message)
