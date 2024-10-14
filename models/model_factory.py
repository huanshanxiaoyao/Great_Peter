import os
from models.llama import LLama3
from models.open_ai import GPT4
from models.deep_seek import DeepSeek2
from models.ali_qianwen import QianWen


class ModelFactory:
    @staticmethod
    def get_model_class(model_name):
        if model_name == "DeepSeek":
            return DeepSeek2(os.getenv("DEEPSEEK_KEY"), os.getenv("DEEPSEEK_URL"))
        elif model_name == "Llama3":
            return LLama3
        elif model_name == "GPT4":
            return GPT4(os.getenv("OPENAI_KEY"))
        elif model_name == "QianWen":
            return QianWen(os.getenv("QIANWEN_KEY"), os.getenv("QIANWEN_URL"))
        else:
            raise Exception(f"Unknown model name {model_name}")
