

class PromptFactory:
    @staticmethod
    def get_title_prompt(message):
        prompt = f" 从下文中获取作者想学习的内容主题: {message}.\
                直接输出答案，不要有多余信息，如果没有输出:No"
        return prompt

    @staticmethod
    def get_chapter_outline_prompt(course_title, chapter_title, chapter_content, chapter_ref):
        outline_prompt = f"我们正在学习 %{course_title}, 今天的章节是%{chapter_title}, \
                主要内容有 %{chapter_content}, 参考文献:%{chapter_ref}, 请认真思考给出本节的教学提纲,\
                建议分3-8个 topic（可视内容多少调整）, 其中每个 topic 包含 title(20字以内) 和 content(200字左右）两部分,\
                返回内容严格采用 json 格式, 第一级目录key:topics,为一个数组，其中每个元素有 title和 content 两个字段"
        return outline_prompt

    @staticmethod
    def get_course_outline_prompt(title, chapters_num):
        outline_prompt = "现在有一个比较重要且有难度的工作，你作为一个指导老师，帮助一个大学生自学%s，\
                使他可以在未来%d 节课，每节花1 个小时左右，对%s的认知提升一个大的台阶，\
                首先 我们要有一个学习提纲，包含学习的目录，以及每一部分要参考的文献；你还要负责细化拆解后面课程，\
                提升学生的学习兴趣和效果，包括最终的考核，好了 现在你来想想如何推进这个工作, 然后输出教学大纲,\
                采用 json 格式, 第一级 key:chapters: 对应一个数组包含每周的学习内容，其中必须有的字段title:本章标题,  content:学习内容，ref:参考文献, 注意保证纯 json 格式，无多余内容，可以被 json 加载" \
                %(title, chapters_num, title)
        return outline_prompt 


if __name__ == "__main__":
    from models.model_factory import ModelFactory
    test_model = ModelFactory.get_model_class("GPT4")
    course_title = "法国历史"
    chapter_title = "中世纪的法国"
    chapter_content = " 法兰克王国的兴起,  加洛林王朝与查理大帝,  封建制度的形成"
    chapter_ref = "《中世纪的结构》, 《查理大帝传》"

    req_content = PromptFactory.get_chapter_outline_prompt(course_title, chapter_title, chapter_content, chapter_ref)
    #req_content = PromptFactory.get_title_prompt("我最近不可能想学习一些法国历史，时间不太多，可能有5个小时")
    print(req_content)
    message = test_model.request(req_content)
    print(message)
